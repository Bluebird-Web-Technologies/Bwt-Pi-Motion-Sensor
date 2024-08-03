from abc import ABC, abstractmethod
from gpiozero import MotionSensor


class Detector(ABC):
    @abstractmethod
    def check_for_change(self):
        pass


class MotionDetector(Detector):
    def __init__(self, pin: int = 4):
        self._pir = MotionSensor(pin)

    def check_for_change(self):
        return self._pir.check_motion


class KeyDetector(Detector):
    def __init__(self, root, trigger="<Return>"):
        self._key_pressed = False
        self._trigger = trigger
        self._root = root
        self._root.bind(self._trigger, self._on_event)

    def _on_event(self, event):
        self._key_pressed = True

    def check_for_change(self):
        if self._key_pressed:
            self._key_pressed = False
            return True
        return False
