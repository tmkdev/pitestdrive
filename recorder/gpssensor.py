#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

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
        packet_dict = {
            'gpo_mode': packet.mode,
            'gps_lon': packet.lon,
            'gps_lat': packet.lat,
            'gps_alt': packet.atl,
            'gps_track': packet.track,
            'gps_hspeed': packet.hspeed,
            'gps_time': packet.time
        }
        return packet_dict

    def run(self):
        while self.running:
            with lock:
                self.current_packet = self.pkt_to_dict(gpsd.get_current())
            time.sleep(0.1)


if __name__ == '__main__':
    gpsp = GpsPoller()  # create the thread
    valid = gpsp.setup()

    gpsp.start()  # start it up
    try:
        while True:
            if gpsp.current_packet:
                try:
                    print(gpsp.current_packet.mode)
                    print(gpsp.current_packet.hspeed)
                    print(gpsp.current_packet.track)
                    print(gpsp.current_packet.position())
                    print(gpsp.current_packet.get_time(local_time=True))
                except:
                    logging.exception('Crrap')

            time.sleep(1)
    except:
        logging.exception('Crap.')
        print('exit.')

    gpsp.running = False
    gpsp.join()
