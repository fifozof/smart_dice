
# MPU register map
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
Device_Address_MPU = 0x68  # MPU6050 device address


# MPU initialization
def MPU_Init(bus):
    # write to sample rate register
    bus.write_byte_data(Device_Address_MPU, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address_MPU, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address_MPU, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address_MPU, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address_MPU, INT_ENABLE, 1)
    # Write registers to enable access to magnetometer
    bus.write_byte_data(Device_Address_MPU, 0x37, 0x02)
    bus.write_byte_data(Device_Address_MPU, 0x6a, 0x00)
    bus.write_byte_data(Device_Address_MPU, 0x6b, 0x00)


# MPU single raw data read
def read_raw_data_MPU(addr, bus):
    # Accelerometer and Gyroscope value are 16-bit
    high = bus.read_byte_data(Device_Address_MPU, addr)
    low = bus.read_byte_data(Device_Address_MPU, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if value > 32768:
        value = value - 65536
    return value


# accelerometer & gyroscope all axis read & convert
def read_MPU(bus):
    acc_x = read_raw_data_MPU(ACCEL_XOUT_H, bus)
    acc_y = read_raw_data_MPU(ACCEL_YOUT_H, bus)
    acc_z = read_raw_data_MPU(ACCEL_ZOUT_H, bus)

    gx = read_raw_data_MPU(GYRO_XOUT_H, bus)
    gy = read_raw_data_MPU(GYRO_YOUT_H, bus)
    gz = read_raw_data_MPU(GYRO_ZOUT_H, bus)

    # converted to m/s^2
    ax = (acc_x / 1670.047) + 7
    ay = (acc_y / 1670.047)
    az = (acc_z / 1670.047) + 1.8

    return ax, ay, az, gx, gy, gz
