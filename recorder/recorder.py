import datetime, time
import logging
import json

import picamera

from motion_sensor import MotionSensor
from gpssensor import GpsPoller

motion = None
gps = None

def setup():
    global motion
    global gps

    motion = MotionSensor()
    valid = motion.setup()

    if motion.sensor_present:
        logging.warning('Motion Sensor Starting')
        motion.start()

    gps = GpsPoller()
    gps.setup()
    gps.start()

def teardown():
    motion.running=False
    if motion.sensor_present:
        motion.join()

    gps.running=False
    if gps.sensor_present:
        gps.join()

def record():
    recordpath = '/home/pi/tracklogs'

    with open('{0}/sensorlog.json'.format(recordpath), 'w') as jsonfile:
        logging.warning('Recording')
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.vflip=True
            camera.rotation=90
            camera.framerate = 30
            camera.start_recording('{0}/sensorlog.h264'.format(recordpath))
            for x in range(200):
                rowdict = {'frame': camera.frame.index,
                           'slot': x,
                           'datetime': str(datetime.datetime.now())}
                try:
                    rowdict['gps_lat'] = gps.current_packet.lat
                    rowdict['gps_lon'] = gps.current_packet.lon
                    rowdict['gps_speed'] = gps.current_packet.hspeed
                    rowdict['gps_alt'] = gps.current_packet.alt
                    rowdict['gps_track'] = gps.current_packet.track
                except:
                    pass
                if motion.sensor_present:
                    rowdict = {**rowdict, **motion.current_reading}

                jsonfile.write(json.dumps(rowdict) + '\n')
                time.sleep(0.1)

if __name__ == '__main__':
    setup()
    record()
    teardown()
