import logging
import sys
import multiprocessing
import datetime, time
import json

import picamera

class Camera(multiprocessing.Process):
    def __init__(self, running_event, recording_event, shared_data_dict, camera_dict, recordpath):
        multiprocessing.Process.__init__(self)
        self.camera_dict = camera_dict
        self.shared_data_dict = shared_data_dict
        self.running_event = running_event
        self.recording_event = recording_event
        self.recordpath = recordpath

    def run(self):
        while self.running_event.is_set():
            if self.recording_event.is_set():
                basename = datetime.datetime.now().strftime('%Y%m%d%H%M')

                jsonfile = '{0}/{1}.json'.format(self.recordpath, basename)
                videofile = '{0}/{1}.h264'.format(self.recordpath, basename)
                self.camera_dict['jsonfile'] = jsonfile
                self.camera_dict['videofile'] = videofile
                self.camera_dict['starttime'] = datetime.datetime.now()

                with open(jsonfile, 'w') as jsonfile:
                    self.camera_dict['status'] = 'recording'
                    logging.warning('Recording to {0}'.format(basename))
                    slot=0
                    with picamera.PiCamera() as camera:
                        camera.resolution = (1920, 1080)
                        camera.rotation = 270
                        camera.framerate = 30
                        camera.start_recording(videofile)
                        while self.recording_event.is_set():
                            rowdict = {'frame': camera.frame.index,
                                        'slot': slot,
                                        'datetime': str(datetime.datetime.now())}
                            rowdict = {**rowdict, **self.shared_data_dict}

                            jsonfile.write(json.dumps(rowdict) + '\n')

                            time.sleep(0.1)
                            slot+=1
                logging.warning("Stopped Recording")

            else:
                self.camera_dict = { 'status': 'stopped' }
                time.sleep(0.1)
