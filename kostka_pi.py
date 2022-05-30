import smbus
import kostka_fsm as fsm
import kostka_MPU as mpu
import kosta_bluetooth as bt
from time import sleep


bus = smbus.SMBus(1)        # I2C bus initialization
mpu.MPU_Init(bus)           # MPU driver initialization
s = bt.bluetooth_Init()     # bluetooth initialization
dice = fsm.DiceFSM()        # finite state machine initialization

# main loop
while 1:
    ax, ay, az, gx, gy, gz = mpu.read_MPU(bus)  # reading accelerometer data
    data = dice.run(ax, ay, az, gx, gy, gz)     # updating fsm
    s.send(bytes([data]))                       # sending data to PC
    print(data)
    sleep(0.01)
