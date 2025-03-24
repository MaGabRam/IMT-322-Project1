import RPi.GPIO as GPIO
import time

# Pines para Motor A
IN1 = 17
IN2 = 18
ENA = 12

# Pines para Motor B
IN3 = 27
IN4 = 22
ENB = 13

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configurar pines de control
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

# PWM (frecuencia 1000Hz)
pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)

# Iniciar PWM con duty cycle 0%
pwmA.start(0)
pwmB.start(0)

def motorA_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)

def motorA_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(speed)

def motorB_forward(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speed)

def motorB_backward(speed):
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmB.ChangeDutyCycle(speed)

def stop_all():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

try:
    print("Motores encendidos...")

    motorA_forward(70)
    motorB_forward(70)
    time.sleep(2)

    motorA_backward(50)
    motorB_backward(50)
    time.sleep(2)

    stop_all()
    print("Motores detenidos")

except KeyboardInterrupt:
    print("Apagando...")
    stop_all()
    GPIO.cleanup()
