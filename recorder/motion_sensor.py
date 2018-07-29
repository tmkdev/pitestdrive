import logging
import sys
import time
import threading

from Adafruit_BNO055 import BNO055


class MotionSensor(threading.Thread):
    def __init__(self, serial_port='/dev/serial0', rst=18):
        threading.Thread.__init__(self)
        self.serial_port = serial_port
        self.rst = rst
        self.current_reading = None
        self.running = True
        self.sensor_present = False
        self.bno = None

    def setup(self):
        try:
            self.bno = BNO055.BNO055(serial_port=self.serial_port, rst=self.rst)
            self.bno.begin()
            status, self_test, error = self.bno.get_system_status()
            logging.info('System status: {0}'.format(status))
            logging.info('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
            if status == 0x01:
                logging.warning('System error: {0}'.format(error))
                logging.warning('See datasheet section 4.3.59 for the meaning.')
                self.sensor_present = False
            else:
                logging.warning("BNO055 set up OK!")
                self.sensor_present = True

            return self.sensor_present
        except:
            self.sensor_present=False
            logging.exception('Failed to initialize BNO055! Is the sensor connected?')

    def run(self):
        while self.running:
            heading, roll, pitch = self.bno.read_euler()
            sys, gyro, accel, mag = self.bno.get_calibration_status()
            temp_c = self.bno.read_temp()
            xl, yl, zl = self.bno.read_linear_acceleration()
            xg, yg, zg = self.bno.read_gravity()
            self.current_reading = {
                'heading': heading,
                'roll': roll,
                'pitch': pitch,
                'sys': sys,
                'gyro': gyro,
                'accel': accel,
                'temp_c': temp_c,
                'xl': xl,
                'yl': yl,
                'zl': zl,
                'xg': xg,
                'yg': yg,
                'zg': zg,
            }

            time.sleep(0.1)


if __name__ == '__main__':
    motion = MotionSensor() # create the thread
    valid = motion.setup()

    if valid:
        motion.start()
    else:
        exit(-1)

    try:
        while True:
            print(motion.current_reading)
            time.sleep(1)

    except:
        logging.exception('Crap.')
        print('exit.')

    motion.running=False
    motion.join()
