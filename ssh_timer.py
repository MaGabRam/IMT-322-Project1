import RPi.GPIO as GPIO
import time
import serial
button1_pin = 19  
aux=3
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
GPIO.setup(button1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

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
archivo2 = "timer.txt"

def read_interval2():
    with open(archivo2, "r") as file:
        line = file.readline().strip()
        if line == '':
            print("⚠️ Archivo vacío, usando valor por defecto.")
            return 1
        try:
            interval = float(line)
            return max(0, interval)
        except ValueError:
            print(f"⚠️ Valor inválido: '{line}', usando 50.")
            return 1   
#UART
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

print("Escuchando...")
msg="buzzer"
try:
    while True:
        timer=read_interval2()
        ser.write(f"{timer}\n".encode('utf-8'))  # Enviar el valor de timer a Tiva
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nSaliendo del programa.")
    ser.close()
