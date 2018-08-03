#! /usr/bin/python
# Based on:
## Written by Dan Mandle http://dan.mandle.me September 2012
## License: GPL 2.0

import os
from time import *
import time
import multiprocessing
import logging

import gpsd

class GpsPoller(multiprocessing.Process):
    def __init__(self, running_event, shared_data_dict):
        multiprocessing.Process.__init__(self)
        self.current_packet = shared_data_dict
        self.sensor_present = True
        self.running = running_event

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
        while self.running.is_set():
            try:
                current_packet = gpsd.get_current()
                self.current_packet.update(self.pkt_to_dict(current_packet))
            except UserWarning:
                logging.warning('Waiting on GPS')

            time.sleep(0.1)


if __name__ == '__main__':
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    running_event = multiprocessing.Event()
    running_event.set()

    gpsp = GpsPoller(shared_data_dict=shared_dict, running_event=running_event)
    valid = gpsp.setup()

    gpsp.start()  # start it up

    try:
        while True:
            print(shared_dict)
            time.sleep(1)
    except:
        logging.exception('Crap.')
        print('exit.')

    running_event.clear()
    gpsp.join()
