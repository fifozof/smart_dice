from math import sqrt
import statistics as st


# finite state machine class
class DiceFSM:
    def __init__(self):

        # possible states
        self.IDLE_STATE = 7
        self.ROLLING_STATE = 8
        self.OUTCOME_STATE = 9
        self.STATE = self.IDLE_STATE

        # buffers for mean calculation
        self.n = 0
        self.k = 0
        self.r = False
        self.acc_buffer = [0.0] * 100
        self.gyro_buffer = [0.0] * 75

    # detecting new roll
    def new_roll(self, ax, ay, az):
        acc_mag = sqrt(ax ** 2 + ay ** 2 + az ** 2)     # magnitude calculation
        self.acc_buffer[self.n] = acc_mag
        mag_mean = st.mean(self.acc_buffer)             # mean magnitude calculation
        self.n += 1
        if self.n == len(self.acc_buffer):              # buffer reset
            self.n = 0
        if mag_mean > 20:                               # new roll condition
            return True
        else:
            return False

    # detecting end of rolling
    def is_steady(self, gx, gy, gz):
        gyro_mag = sqrt(gx ** 2 + gy ** 2 + gz ** 2)     # magnitude calculation
        self.gyro_buffer[self.k] = gyro_mag
        mag_mean = st.mean(self.gyro_buffer)             # mean magnitude calculation
        self.k += 1
        # print(mag_mean)
        if self.k == len(self.gyro_buffer):              # buffer reset
            self.k = 0
        if mag_mean < 200:                               # steady condition
            return True
        else:
            return False

    # detect dice wall
    def dice_value(self, ax, ay, az):
        if ax > 8:                          # conditions for each wall
            return 1
        if ax < -8:
            return 6
        if ay > 8:
            return 2
        if ay < -8:
            return 5
        if az > 8:
            return 4
        if az < -8:
            return 3
        else:
            return 0

    # detecting start of rolling
    def is_rolling(self, gx, gy, gz):
        gyro_mag = sqrt(gx ** 2 + gy ** 2 + gz ** 2)     # magnitude calculation
        self.gyro_buffer[self.k] = gyro_mag
        mag_mean = st.mean(self.gyro_buffer)             # mean magnitude calculation
        self.k += 1
        # print(mag_mean)
        if self.k == len(self.gyro_buffer):              # buffer reset
            self.k = 0
        if mag_mean > 2000:                               # start rolling condition
            return True
        else:
            return False

        # updating fsm
    def run(self, ax, ay, az, gx, gy, gz):

        # Waiting for roll
        if self.STATE == self.IDLE_STATE:
            self.r = False
            if self.is_rolling(gx, gy, gz):
                self.STATE = self.ROLLING_STATE
                return self.STATE
            else:
                self.STATE = self.IDLE_STATE
                return self.STATE

        # Rolling
        elif self.STATE == self.ROLLING_STATE:
            if self.is_steady(gx, gy, gz):
                self.STATE = self.OUTCOME_STATE
                self.gyro_buffer = [0.0] * 75
                return self.STATE
            else:
                self.STATE = self.ROLLING_STATE
                return self.STATE

        # Checking outcome
        elif self.STATE == self.OUTCOME_STATE:
            if self.new_roll(ax, ay, az):
                self.STATE = self.IDLE_STATE
                self.acc_buffer = [0.0] * 100
                return self.STATE
            elif not self.r:
                self.STATE = self.OUTCOME_STATE
                self.r = True
                return self.dice_value(ax, ay, az)
            else:
                self.STATE = self.OUTCOME_STATE
                return 0

        # Error
        else:
            print("Error")
