#引入库
import serial
import RPi.GPIO as GPIO#树莓派引脚库
import struct
import time


from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus.constants as cst
EN_485 = 4
GPIO.setmode(GPIO.BCM)#设置树莓派引脚模式为BCM编码模式
GPIO.setup(EN_485,GPIO.OUT)#设置引脚为输出模式
GPIO.output(EN_485,GPIO.HIGH)#设置引脚为高电平输出
client = ModbusClient(
    method='rtu',
    port='/dev/ttyAMA0',  # Adjust the port name as necessary
    baudrate=9600,
    timeout=1,
    stopbits=1,
    bytesize=8,
    parity='N'
)

# Connect to the client
connection = client.connect()
if not connection:
    print("Failed to connect to the serial port")
    exit()

# Read the values from the specified registers
start_address = 0x0E
number_of_registers = 2
unit_id = 1  # Slave address

read_values = client.read_holding_registers(start_address, number_of_registers, unit=unit_id)

# Check if the read was successful and print the values
if not read_values.isError():
    print("Read values:", read_values.registers)
else:
    print("Error reading values")

# Close the connection
client.close()