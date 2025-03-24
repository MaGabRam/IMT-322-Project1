import RPi.GPIO as GPIO
import time
import serial
#motores
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
#Movimientos
def motorA_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(speed)
def motorB_forward(speed):
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmB.ChangeDutyCycle(speed)
GPIO.setwarnings(False)
archivo = "duty.txt"

def read_interval():
    with open(archivo, "r") as file:
        line = file.readline().strip()
        if line == '':
            print("⚠️ Archivo vacío, usando valor por defecto.")
            return 50
        try:
            interval = float(line)
            return max(0, interval)
        except ValueError:
            print(f"⚠️ Valor inválido: '{line}', usando 50.")
            return 50
#UART
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

print("Escuchando...")

try:
    while True:
        duty=read_interval()
        if ser.in_waiting > 0:
            raw = ser.readline()
            try:
                data = raw.decode('utf-8').rstrip()
                print("Tiva dice:", data)
                if data == "motor1":
                    print(duty)
                    motorA_forward(duty)
                elif data == "motor2":
                    print(duty)
                    motorB_forward(duty)
                else:
                    pwmA.ChangeDutyCycle(0)
                    pwmB.ChangeDutyCycle(0)
                    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
            except UnicodeDecodeError:
                print("⚠️ Datos corruptos ignorados:", raw)
except KeyboardInterrupt:
    print("\nSaliendo del programa.")
    ser.close()
