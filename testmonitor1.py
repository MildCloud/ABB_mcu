import serial
import struct
import RPi.GPIO as GPIO
import time
import crcmod

# Setup RS-485 control pin
EN_485 = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_485, GPIO.OUT)
GPIO.output(EN_485, GPIO.HIGH)

# Configure the serial port
port = "/dev/ttyAMA0"
ser = serial.Serial(
    port=port,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=2  # Further increased timeout
)

# Check if the serial port is open
if ser.isOpen():
    print("Serial port opened successfully")

# Function to calculate CRC16
def calc_crc(data):
    crc16 = crcmod.predefined.mkCrcFun('modbus')
    return crc16(data).to_bytes(2, byteorder='little')

# Form the Modbus RTU request
slave_address = 0x01
function_code = 0x03
start_address = 0x000E
num_registers = 0x0002

# Pack the request
request = struct.pack('>BBHH', slave_address, function_code, start_address, num_registers)
# Add CRC to the request
crc = calc_crc(request)
request += crc

# Send the request
GPIO.output(EN_485, GPIO.HIGH)  # Enable RS-485 transmission
ser.write(request)
ser.flush()
time.sleep(0.1)  # Ensure the data is sent
GPIO.output(EN_485, GPIO.LOW)  # Disable RS-485 transmission

# Read the response
response = ser.read(7 + 2 * num_registers)  # 7 bytes header + 2 bytes per register
if len(response) == 0:
    print("No response received")
else:
    print("Response:", response)

# Close the serial port
ser.close()

# Example of parsing the response
if len(response) >= 5:
    slave_id, function, byte_count = struct.unpack('>BBB', response[:3])
    values = struct.unpack('>' + 'H' * num_registers, response[3:-2])
    crc_received = response[-2:]
    crc_calculated = calc_crc(response[:-2])

    if crc_received == crc_calculated:
        print(f"Slave ID: {slave_id}, Function: {function}, Byte Count: {byte_count}")
        print("Values:", values)
    else:
        print("CRC check failed")
else:
    print("Incomplete response received")
