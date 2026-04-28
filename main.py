import cv2
import time
import os
from ultralytics import YOLO
from core.hardware import HardwareControl
from core.gestures import check_hands_up
from utils.visualizer import HeatmapGenerator
from utils.tg_bot import send_telegram_alert  # Теперь это наш локальный архив

# --- CONFIG ---
VIDEO_URL = "http://192.168.50.8:4747/video"
MODEL_PATH = "models/yolov8n-pose.pt"
REPORT_PATH = "images/heatmap_report.jpg"

def main():
    # Инициализация железа и нейросети
    hw = HardwareControl()
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(VIDEO_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # Инициализация аналитики
    heatmap = HeatmapGenerator()

    last_report_time = time.time()
    last_alert_time = 0      # Таймер для защиты от спама записями
    alert_cooldown = 10      # Записывать не чаще чем раз в 10 секунд
    intruder_counter = 0     # Номер нарушения
    frame = None 

    print("\n" + "="*40)
    print("--- SMART EYE 2.5: LOCAL ARCHIVE MODE ---")
    print("="*40)
    print(f"Камера: {VIDEO_URL}")
    print("Логи сохраняются в images/evidence/")

    try:
        while True:
            # Очистка буфера для свежего кадра
            for _ in range(4): cap.grab()
            ret, current_frame = cap.retrieve()
            if not ret:
                continue

            # Поворот кадра
            frame = cv2.rotate(current_frame, cv2.ROTATE_90_CLOCKWISE)

            # Нейросеть (Pose Estimation)
            results = model(frame, imgsz=160, conf=0.5, verbose=False)

            if len(results[0].keypoints) > 0:
                keypoints = results[0].keypoints.xy[0]

                # Добавляем точку в тепловую карту (точка 11 - таз)
                if len(keypoints) > 11:
                    x, y = int(keypoints[11][0]), int(keypoints[11][1])
                    if x > 0 and y > 0:
                        heatmap.add_point(x, y, frame.shape)

                # Распознавание жеста
                hands_up = check_hands_up(results[0].keypoints)
                if hands_up:
                    if hw.is_active: print("🙌 ЖЕСТ: ТРЕВОГА СНЯТА")
                    hw.set_alert(False)
                else:
                    if not hw.is_active: 
                        print("🚨 ОБНАРУЖЕН НАРУШИТЕЛЬ!")
                        intruder_counter += 1
                    hw.set_alert(True)

                    # ЛОКАЛЬНАЯ ЗАПИСЬ (если прошло больше 10 сек)
                    current_time = time.time()
                    if current_time - last_alert_time > alert_cooldown:
                        temp_path = "images/last_intruder.jpg"
                        cv2.imwrite(temp_path, frame)
                        
                        # Вызываем функцию сохранения в архив
                        if send_telegram_alert(temp_path, intruder_counter):
                            last_alert_time = current_time
            else:
                hw.set_alert(False)

            # Периодическое сохранение хитмапа (раз в 30 сек)
            if time.time() - last_report_time > 30:
                report_img = heatmap.get_overlay(frame)
                cv2.imwrite(REPORT_PATH, report_img)
                
                # Сохраняем копию хитмапа в архив с меткой времени
                t_stamp = time.strftime("%H-%M-%S")
                cv2.imwrite(f"images/evidence/heatmap_{t_stamp}.jpg", report_img)
                
                print(f"📊 Тепловая карта обновлена и добавлена в архив")
                last_report_time = time.time()

    except KeyboardInterrupt:
        print("\n🛑 Ручной останов...")
        if frame is not None:
            final_report = heatmap.get_overlay(frame)
            cv2.imwrite(REPORT_PATH, final_report)
            cv2.imwrite(f"images/evidence/final_heatmap.jpg", final_report)
            print("✅ Все финальные отчеты сохранены.")

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

    finally:
        hw.cleanup()
        cap.release()
        print("Система выключена.")

if __name__ == "__main__":
    main()
