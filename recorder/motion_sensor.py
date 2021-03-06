import logging
import sys
import time
import multiprocessing

from Adafruit_BNO055 import BNO055


class MotionSensor(multiprocessing.Process):
    def __init__(self, shared_data_dict, running_event, serial_port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AH02JLPE-if00-port0'):
        multiprocessing.Process.__init__(self)
        self.serial_port = serial_port
        self.current_reading = shared_data_dict
        self.running = running_event
        self.sensor_present = False
        self.bno = None

    def setup(self):
        try:
            self.bno = BNO055.BNO055(serial_port=self.serial_port)
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
            self.sensor_present = False
            logging.exception('Failed to initialize BNO055! Is the sensor connected?')

    def run(self):
        while self.running.is_set():
            heading, roll, pitch = self.bno.read_euler()
            sys, gyro, accel, mag = self.bno.get_calibration_status()
            temp_c = self.bno.read_temp()
            xl, yl, zl = self.bno.read_linear_acceleration()
            xg, yg, zg = self.bno.read_gravity()
            self.current_reading.update({
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
                })

            time.sleep(0.05)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    running_event = multiprocessing.Event()
    running_event.set()


    motion = MotionSensor(shared_data_dict=shared_dict, running_event=running_event)  # create the thread
    valid = motion.setup()

    if valid:
        motion.start()
    else:
        exit(-1)

    try:
        while True:
            logging.warning(shared_dict)
            time.sleep(1)

    except:
        logging.exception('Something Failed...')

    running_event.clear()
    motion.join()
