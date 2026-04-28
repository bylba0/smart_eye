import os
from datetime import datetime

# Указываем ПРЯМОЙ путь к папке (замени egor на свое имя пользователя, если оно другое)
EVIDENCE_DIR = "/home/egor/smart_eye/images/evidence"

def send_telegram_alert(photo_path, count):
    try:
        # Создаем папку, если её нет (с полным путем)
        if not os.path.exists(EVIDENCE_DIR):
            os.makedirs(EVIDENCE_DIR, exist_ok=True)

        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"intruder_{count}_{timestamp}.jpg"
        save_path = os.path.join(EVIDENCE_DIR, filename)

        # Читаем фото, которое сохранил main.py, и пересохраняем в архив
        import shutil
        shutil.copy(photo_path, save_path)

        print(f"✅ Файл скопирован в архив: {save_path}")
        return True
    except Exception as e:
        print(f"❌ Ошибка архивации: {e}")
        return False
