import board
import busio
import adafruit_pca9685
import time

class Servo:

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.hat = adafruit_pca9685.PCA9685(i2c, address=0x54)
        self.hat.frequency = 50 #50 Hz
        #in1 needs to be high, in2 needs to be low
        self.a1=self.hat.channels[4]
        self.a2=self.hat.channels[3]
        self.b2=self.hat.channels[5]
        self.b1=self.hat.channels[6]

        self.servo1 = self.hat.channels[2]
        self.servo2 = self.hat.channels[7]

        #matlabs polyfit used to find coefficients of line to convert angle to pwm
        self.m = 51.11
        self.b = 6500


    def turn_on(self):
        self.a1.duty_cycle = 0x0000
        self.b1.duty_cycle = 0x0000
        self.a2.duty_cycle = 0xffff
        self.b2.duty_cycle = 0xffff

    def turn_off(self):
        self.a1.duty_cycle = 0x0000
        self.b1.duty_cycle = 0x0000
        self.a2.duty_cycle = 0x0000
        self.b2.duty_cycle = 0x0000

        #1ms duty cycle = -90d -> 0x0ccc or 3276
        #1.5ms duty cycle = 0d -> 0x1333
        #2ms duty cycle = 90d  -> 0x1999 or 6553

    def test(self):

        #testing shows range from ~4200 to ~8900
        j=0
        while(j<1):
            for i in range(4000, 9500, 20):
                print(i)
                self.servo1.duty_cycle = i
                time.sleep(0.5)
            for i2 in range(4500, 9000, 200):
                print(i2)
                self.servo2.duty_cycle = i2
                time.sleep(0.5)
            j += 1

    #input angle ranges from -45d to 45d
    #servo datasheet says range is 180d but it is not
    #also have no way of measuring angle of servos so this is rough estimate
    def set_Xangle(self, theta):
        pwm = round(self.m*theta + self.b)
        self.servo1.duty_cycle = pwm

    def set_Yangle(self, theta):
        pwm = round(-self.m*theta + self.b)
        self.servo2.duty_cycle = pwm

if __name__ == "__main__":
    a = Servo()
    a.turn_on()
    a.test()
    a.turn_off()
