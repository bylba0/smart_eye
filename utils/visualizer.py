import numpy as np
import cv2

class HeatmapGenerator:
    def __init__(self):
        self.heatmap_accumulator = None # Пока не знаем размер
        
    def add_point(self, x, y, frame_shape):
        """Добавляет точку, создавая карту под размер кадра при первом вызове"""
        if self.heatmap_accumulator is None:
            self.heatmap_accumulator = np.zeros(frame_shape[:2], dtype=np.float32)
        
        cv2.circle(self.heatmap_accumulator, (int(x), int(y)), 30, 0.5, -1)
        self.heatmap_accumulator = cv2.GaussianBlur(self.heatmap_accumulator, (25, 25), 0)

    def get_overlay(self, frame):
        if self.heatmap_accumulator is None:
            return frame # Возвращаем оригинал, если данных еще нет
            
        heatmap_norm = cv2.normalize(self.heatmap_accumulator, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_norm = np.uint8(heatmap_norm)
        heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
        
        # Теперь размеры гарантированно совпадут
        result = cv2.addWeighted(frame, 0.7, heatmap_color, 0.3, 0)
        return result
