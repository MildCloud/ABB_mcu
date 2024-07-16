#引入库
import serial
import modbus_tk.modbus_rtu as rtu
import modbus_tk.defines as cst
import RPi.GPIO as GPIO#树莓派引脚库
import struct

#设置串口
EN_485 = 4
GPIO.setmode(GPIO.BCM)#设置树莓派引脚模式为BCM编码模式
GPIO.setup(EN_485,GPIO.OUT)#设置引脚为输出模式
GPIO.output(EN_485,GPIO.LOW)#设置引脚为高电平输出

ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,parity="N")
if ser.isOpen():
    print("Serial Opened")
#设置电脑端为主机（Master）
master = rtu.RtuMaster(ser)
master.set_timeout(1.0)
master.set_verbose(True)

#float 读取
# 读取寄存器值，从地址0x0106开始读取4个寄存器（长整型）
f_start_address_fwd = 0x000E
f_start_address_bck = 0x0010
f_num_registers = 2

# 读取寄存器值，从地址0x0106开始读取4个寄存器（长整型）
start_address_fwd = 0x0106
start_address_bck = 0x0108
num_registers = 4

data_format = 0 #0为float（单位为kWh), 1为long(单位为10Wh)

# 读取寄存器值
if data_format == 0:
    read_values_fwd = master.execute(195, cst.HOLDING_REGISTERS, f_start_address_fwd, f_num_registers)
    read_values_bck = master.execute(195, cst.HOLDING_REGISTERS, f_start_address_bck, f_num_registers)
else:
    read_values_fwd = master.execute(195, cst.HOLDING_REGISTERS, start_address_fwd, num_registers)
    read_values_bck = master.execute(195, cst.HOLDING_REGISTERS, start_address_bck, num_registers)

def convert_to_float(high, low):
    # 将两个16位寄存器值合并为一个32位整数并转换为浮点数
    combined = (high << 16) + low
    float_value = struct.unpack('>f', struct.pack('>I', combined))[0]
    return float_value


def convert_to_long(values):
    # 将4个16位寄存器值合并为一个64位整数
    combined = (values[0] << 48) + (values[1] << 32) + (values[2] << 16) + values[3]
    return combined

# 将寄存器值转换为长整型
long_value_fwd = convert_to_long(read_values_fwd)
long_value_bck = convert_to_long(read_values_bck)
print ("Long value (forward):", long_value_fwd)
print ("Long value (backward):", long_value_bck)
