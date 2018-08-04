import gpssensor
import logging
import time

if __name__ == '__main__':
  gpsp = gpssensor.GpsPoller() # create the thread
  valid = gpsp.setup()

  gpsp.start() # start it up
  try:
    while True:
      if gpsp.current_packet:
        print(dict(gpsp.current_packet))

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

  gpsp.running=False
  gpsp.join()


