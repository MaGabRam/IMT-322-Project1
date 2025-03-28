# esto esperamoa que ya no se desconfigure
# raspi -config  -> abre interfaz para habilitar o desahilitar, se habilita lo de USB


import RPi.GPIO as GPIO
import time
import serial # LIBRERIA PARA COMUNICACION SERIAL

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
# esto es una funcion, debe tener formula, directamente lo convierte Hz
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
#UART---------------------------------------------------------------------------------------------------------------------

#la comunicacion serial se vuelve una variable y poner puerto deonde se conecta la TIVA
#SE PONE sudo ls /dev/tty Y deberia salir en nombre, puede cambiar entonces hay que revisar is es que no compila: no se encuentra el puerto
ser = serial.Serial('/dev/ttyACM0', 9600) # con la misma velocidade de baudios
ser.reset_input_buffer() # esto no entiendo pero maso como que limpia lo que habia

print("Escuchando...")
msg="buzzer"
try:
    while True:
        # el uart es esto---------------------------------------------------------------
        duty=read_interval() # si se recibe algo se ejecuta lo siguiente
        if ser.in_waiting > 0:
            raw = ser.readline() # aqui lee todo la linea
            try: 
                data = raw.decode('utf-8').rstrip() # utf-8 es un formato de codificacion : universal algo # rstrip limipa la linea
                print("Tiva dice:", data)
                if data == "motor1":
                    print(duty)
                    motorA_forward(duty)
                elif data == "motor2":
                    print(duty)
                    motorB_forward(duty)
        # hasta aqui uart ---------------------------------------------------------------
            except UnicodeDecodeError:
                print("⚠️ Datos corruptos ignorados:", raw)
        # s eenvian datos desde el uart desde la rasp:
        if GPIO.input(button1_pin) == GPIO.LOW:
            print("Button 1 on")
            # este se ejecuta solo una vez  por eso mas abajo se pone off
            ser.write("buzzer\n".encode('utf-8'))  # Enviar a Tiva
            aux=1
            time.sleep(0.2)
        elif aux==1:
            print("Button 1 off")
            ser.write("off\n".encode('utf-8'))  # Enviar a Tiva
            aux=0
            time.sleep(0.2)
except KeyboardInterrupt:
    print("\nSaliendo del programa.")
    ser.close()
