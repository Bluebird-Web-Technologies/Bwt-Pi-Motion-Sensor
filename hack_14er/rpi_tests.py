from gpiozero import MotionSensor, LED

LED_PIN = 17
PIR_PIN = 4

pir = MotionSensor(PIR_PIN)
led = LED(LED_PIN)


def print_test():
    pir.wait_for_motion()
    print("You moved")
    pir.wait_for_no_motion()


def motion_detected_action():
    print("Motion detected")
    led.on()
    led.source_delay = 3


def led_test():
    pir.when_motion = motion_detected_action
    pir.when_no_motion = led.off


if __name__ == "__main__":
    led_test()
