import logging
import sys
import time
import multiprocessing

import can4python as can

class CanBus_Sensor(multiprocessing.Process):
    def __init__(self, shared_data_dict, running_event, kcd, canbus='can0', ):
        multiprocessing.Process.__init__(self)
        self.canbus = canbus
        self.current_reading = shared_data_dict
        self.running = running_event
        self.sensor_present = False
        self.kcd = kcd
        self.bus = None

    def setup(self):
        try:
            self.bus = can.CanBus.from_kcd_file(self.kcd, self.canbus)
            self.sensor_present = True

            return self.sensor_present
        except:
            self.sensor_present = False
            logging.exception('Failed to initialize canbus..')

    def run(self):
        while self.running.is_set():
            received_signalvalues = bus.recv_next_signals()
            self.current_reading.update(received_signalvalues)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    running_event = multiprocessing.Event()
    running_event.set()


    canbus_sensor = CanBus_Sensor(shared_data_dict=shared_dict, running_event=running_event, canbus='can0', kcd='kcd/gm_global_a_hs.kcd') 
    valid = canbus_sensor.setup()

    if valid:
        canbus_sensor.start()
    else:
        exit(-1)

    try:
        while True:
            logging.warning(shared_dict)
            time.sleep(1)

    except:
        logging.exception('Something Failed...')

    running_event.clear()
    canbus_sensor.join()
