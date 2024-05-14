import RPi.GPIO as GPIO
from time import sleep, time
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB, 100);
        self.pwmB.start(0);
        self.last_stop_time = 0
        self.start_delay = 20  # Delay in seconds before allowing the motor to start again
        self.allow_start = True

    def move(self,speed=0.5,turn=0,t=0):
        # Check if the motor is allowed to start
        if self.allow_start:
            speed *=100
            turn *=100
            leftSpeed = speed - turn
            rightSpeed = speed + turn
            if leftSpeed>100: leftSpeed=100
            elif leftSpeed<-100: leftSpeed= -100
            if rightSpeed>100: rightSpeed=100
            elif rightSpeed<-100: rightSpeed= -100

            self.pwmA.ChangeDutyCycle(abs(leftSpeed))
            self.pwmB.ChangeDutyCycle(abs(rightSpeed))

            if leftSpeed>0:
                GPIO.output(self.In1A,GPIO.HIGH)
                GPIO.output(self.In2A,GPIO.LOW)
            else:
                GPIO.output(self.In1A,GPIO.LOW)
                GPIO.output(self.In2A,GPIO.HIGH)

            if rightSpeed>0:
                GPIO.output(self.In1B,GPIO.HIGH)
                GPIO.output(self.In2B,GPIO.LOW)
            else:
                GPIO.output(self.In1B,GPIO.LOW)
                GPIO.output(self.In2B,GPIO.HIGH)

            sleep(t)
        else:
          print("Motor start not allowed due to delay")

    def stop(self,t=0):
        print("Stopping motor")
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        self.last_stop_time = time()  # Record the time when the motor was last stopped
        self.allow_start = False  # Disable motor start
        # Schedule re-enablement of motor start after delay
        threading.Timer(self.start_delay, self.enable_start).start()

    def enable_start(self):
        print("Motor start allowed")
        self.allow_start = True  # Allow motor start
