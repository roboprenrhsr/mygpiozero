from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero.exc import OutputDeviceBadValue

class Motor():
    def __init__(self, forward, backward, pwm, *, pin_factory=None):
        self.forward_device = DigitalOutputDevice(forward, pin_factory=pin_factory)
        self.backward_device = DigitalOutputDevice(backward, pin_factory=pin_factory)
        self.pwm_device = PWMOutputDevice(pwm, pin_factory=pin_factory)

    @property
    def value(self):
        return (self.forward_device.value - self.backward_device.value) * self.pwm_device.value

    @value.setter
    def value(self, value):
        if not -1 <= value <= 1:
            raise OutputDeviceBadValue("Motor value must be between -1 and 1")
        if value > 0:
            try:
                self.forward(value)
            except ValueError as e:
                raise OutputDeviceBadValue(e)
        elif value < 0:
            try:
               self.backward(-value)
            except ValueError as e:
                raise OutputDeviceBadValue(e)
        else:
            self.stop()

    @property
    def is_active(self):
        return self.value != 0

    def forward(self, speed=1):
        if not 0 <= speed <= 1:
            raise ValueError('forward speed must be between 0 and 1')
        self.backward_device.off()
        self.forward_device.on()
        self.pwm_device.value = speed

    def backward(self, speed=1):
        if not 0 <= speed <= 1:
            raise ValueError('backward speed must be between 0 and 1')
        self.forward_device.off()
        self.backward_device.on()
        self.pwm_device.value = speed

    def reverse(self):
        self.value = -self.value

    def stop(self, mode=1):
        if mode == 1:
            self.pwm_device.value = 0
        elif mode == 2:
            self.forward_device.on()
            self.backward_device.on()
        elif mode == 3:
            self.forward_device.off()
            self.backward_device.off()

    def close(self):
        self.forward_device.close()
        self.backward_device.close()
        self.pwm_device.close()

class Robot():
    def __init__(self, left, right):
        self.left_motor = left
        self.right_motor = right

    @property
    def value(self):
        return (self.left_motor.value, self.right_motor.value)

    @value.setter
    def value(self, value):
        self.left_motor.value, self.right_motor.value = value

    def forward(self, speed=1, *, curve_left=0, curve_right=0):
        if not 0 <= curve_left <= 1:
            raise ValueError('curve_left must be between 0 and 1')
        if not 0 <= curve_right <= 1:
            raise ValueError('curve_right must be between 0 and 1')
        if curve_left != 0 and curve_right != 0:
            raise ValueError("curve_left and curve_right can't be used at the same time")
        self.left_motor.forward(speed * (1 - curve_left))
        self.right_motor.forward(speed * (1 - curve_right))

    def backward(self, speed=1, *, curve_left=0, curve_right=0):
        if not 0 <= curve_left <= 1:
            raise ValueError('curve_left must be between 0 and 1')
        if not 0 <= curve_right <= 1:
            raise ValueError('curve_right must be between 0 and 1')
        if curve_left != 0 and curve_right != 0:
            raise ValueError("curve_left and curve_right can't be used at the same time")
        self.left_motor.backward(speed * (1 - curve_left))
        self.right_motor.backward(speed * (1 - curve_right))

    def left(self, speed=1):
        self.right_motor.forward(speed)
        self.left_motor.backward(speed)

    def right(self, speed=1):
        self.left_motor.forward(speed)
        self.right_motor.backward(speed)

    def reverse(self):
        self.left_motor.reverse()
        self.right_motor.reverse()

    def stop(self, mode=1):
        self.left_motor.stop(mode)
        self.right_motor.stop(mode)

    def close(self):
        self.left_motor.close()
        self.right_motor.close()
