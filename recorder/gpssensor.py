#! /usr/bin/python
# Based on:
## Written by Dan Mandle http://dan.mandle.me September 2012
## License: GPL 2.0


import os
from time import *
import time
import threading
import logging

import gpsd

lock = threading.Lock()


class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_packet = None
        self.running = True
        self.sensor_present = True

    def setup(self):
        gpsd.connect()

    def pkt_to_dict(self, packet):
        try:
            packet_dict = {
                'gps_mode': packet.mode,
                'gps_lon': packet.lon,
                'gps_lat': packet.lat,
                'gps_alt': packet.alt,
                'gps_track': packet.track,
                'gps_hspeed': packet.hspeed,
                'gps_time': packet.time
            }
        except:
            packet_dict = {}

        return packet_dict

    def run(self):
        while self.running:
            try:
                current_packet = gpsd.get_current()
                with lock:
                    self.current_packet = self.pkt_to_dict(current_packet)
            except UserWarning:
                logging.warning('Waiting on GPS')

            time.sleep(0.1)


if __name__ == '__main__':
    gpsp = GpsPoller()  # create the thread
    valid = gpsp.setup()

    gpsp.start()  # start it up
    try:
        while True:
            if gpsp.current_packet:
                try:
                    print(gpsp.current_packet)
                except:
                    logging.exception('Crrap')

            time.sleep(1)
    except:
        logging.exception('Crap.')
        print('exit.')

    gpsp.running = False
    gpsp.join()
