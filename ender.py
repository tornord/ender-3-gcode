import serial
import time

# Change this to your printer port:
# Linux: /dev/ttyUSB0 or /dev/ttyACM0
# macOS: /dev/cu.usbmodem...
# Windows: COM3, COM4, etc.
PORT = "/dev/ttyUSB0"

BAUDRATE = 115200

# Open serial connection
printer = serial.Serial(PORT, BAUDRATE, timeout=1)

# Give the printer time to reset after serial connect
time.sleep(1)

def send_gcode(cmd):
    print(">>", cmd)

    # Send command with newline
    printer.write((cmd + "\n").encode())

    # Read responses
    while True:
        response = printer.readline().decode(errors="ignore").strip()

        if response:
            print("<<", response)

        # Most Marlin firmware replies with 'ok'
        if response == "ok" or response == "echo:TF card ok":
            break

# Wake up / clear startup text
printer.flushInput()

send_gcode("M104 S0") # Set no nozzle temp
send_gcode("M140 S0") # Bed temp
send_gcode("G92 X0 Y0 Z0") # Reset x y z
send_gcode("G92 E0") # Reset extruder
send_gcode("G1 Z5 F500")

with open("abc.gcode") as f:
    for line in f:
        cmd = line.strip()
        if cmd:
            send_gcode(cmd)

printer.close()