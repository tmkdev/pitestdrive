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

    def run():
        while self.running_event.is_set():
            if self.recording_event.is_set():
                basename = datetime.datetime.now().strftime('%Y%m%d%H%M')

                jsonfile = f'{self.recordpath}/{basename}.json'
                videofile = f'{self.recordpath}/{basename}.h264'
                camera_dict['jsonfile'] = jsonfile
                camera_dict['videofile'] = videofile

                with open(jsonfile, 'w') as jsonfile:
                    camera_dict['status'] = 'recording'
                    logging.warning(f'Recording to {basename}')
                    slot=0
                    with picamera.PiCamera() as camera:
                        camera.resolution = (1920, 1080)
                        camera.rotation = 270
                        camera.framerate = 30
                        camera.start_recording(videofile).str
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
                camera_dict['status'] = 'stopped'
                camera_dict['jsonfile'] = None
                camera_dict['videofile'] = None
                time.sleep(0.1)
