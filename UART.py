import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.reset_input_buffer()

print("Escuchando...")

try:
    while True:
        if ser.in_waiting > 0:
            raw = ser.readline()
            try:
                data = raw.decode('utf-8').rstrip()
                print("Tiva dice:", data)
                ser.write((data + "\n").encode())
            except UnicodeDecodeError:
                print("⚠️ Datos corruptos ignorados:", raw)
except KeyboardInterrupt:
    print("\nSaliendo del programa.")
    ser.close()
