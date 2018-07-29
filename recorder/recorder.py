import picamera
import csv
import datetime, time
import logging

from motion_sensor import MotionSensor
from gpssensor import GpsPoller
from gpiohandler import GpioHandler

gpiohandler  = None
motion = None
gps = None

def setup():
    global gpiohandler
    global motion
    global gps

    gpiohandler = GpioHandler()
    gpiohandler.set_all(True)
    time.sleep(0.5)
    gpiohandler.set_all(False)

    gpiohandler.set_led(GpioHandler.green1)

    motion = MotionSensor()
    valid = motion.setup()

    if motion.sensor_present:
        logging.warning('Motion Sensor Starting')
        motion.start()
        gpiohandler.set_led(GpioHandler.green2)

    gps = GpsPoller()
    gps.setup()
    gps.start()

def teardown():
    motion.running=False
    if motion.sensor_present:
        gpiohandler.clear_led(GpioHandler.green2)
        motion.join()

    gps.running=False
    if gps.sensor_present:
        gps.join()

    gpiohandler.set_all(False)

def record():
    gpiohandler.set_led(GpioHandler.red)
    with open('sensorlog.csv', 'w') as csvfile:
        csvheader = 'frame,dataindex,datetime,lat,lon,hspeed,alt,track,gpstime,mode'
        if motion.sensor_present:
            csvheader += ',heading,pitch,roll,sys,gyro,accel,temp_c,xl,yl,zl,xg,yg,zg'
        csvfile.write(csvheader + '\n')
        logging.warning('Recording')
        with picamera.PiCamera() as camera:
            camera.resolution = (1920, 1080)
            camera.vflip=True
            camera.framerate = 24
            camera.start_recording('my_video.h264')
            for x in range(200):
                row = "{0},{1},{2}".format(camera.frame.index, x, datetime.datetime.now())
                try:
                    row += ",{0},{1},{2},{3},{4},{5},{6}".format(gps.current_packet.lat,  gps.current_packet.lon, gps.current_packet.hspeed, gps.current_packet.alt, gps.current_packet.track, gps.current_packet.get_time(local_time=True), gps.current_packet.mode)
                except:
                    #logging.exception('gps..')
                    row += ",,,,,,,"
                if motion.sensor_present:
                    row += ",{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}".format(motion.current_reading['heading'],
                                                motion.current_reading['pitch'],
                                                motion.current_reading['roll'],
                                                motion.current_reading['sys'],
                                                motion.current_reading['gyro'],
                                                motion.current_reading['accel'],
                                                motion.current_reading['temp_c'],
                                                motion.current_reading['xl'],
                                                motion.current_reading['yl'],
                                                motion.current_reading['xl'],
                                                motion.current_reading['xg'],
                                                motion.current_reading['yg'],
                                                motion.current_reading['zg'])
                row += '\n'
                csvfile.write(row)
                time.sleep(0.1)

    gpiohandler.clear_led(GpioHandler.red)



if __name__ == '__main__':
    setup()
    record()
    teardown()
