import RPi.GPIO as GPIO

class HardwareControl:
    def __init__(self, green=17, red=27, buz=22):
        self.pins = {'GREEN': green, 'RED': red, 'BUZ': buz}
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(list(self.pins.values()), GPIO.OUT)
        
        # Флаг текущего состояния (чтобы main.py мог его проверять)
        self.is_active = False 

    def set_alert(self, is_active):
        """Включает красный свет и зуммер, если активна тревога"""
        if is_active:
            GPIO.output(self.pins['GREEN'], False)
            GPIO.output(self.pins['RED'], True)
            GPIO.output(self.pins['BUZ'], True)
        else:
            GPIO.output(self.pins['GREEN'], True)
            GPIO.output(self.pins['RED'], False)
            GPIO.output(self.pins['BUZ'], False)
        
        # Обновляем внутренний флаг
        self.is_active = is_active

    def cleanup(self):
        """Безопасное выключение GPIO"""
        GPIO.cleanup()
