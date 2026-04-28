import csv
import time
import os

def log_event(photo_path, log_file="security_log.csv"):
    """Записывает событие и путь к фото в CSV файл"""
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Photo', 'Status'])
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), photo_path, 'DETECTION'])

