import time
from flask import Flask
from multiprocessing import Process, Manager

from views.hello import hello
from views.stats import stats

from motion_sensor import MotionSensor

def create_app(record_event, shared_dict, debug=False):
    app = Flask(__name__)
    app.debug = debug

    app.register_blueprint(hello)
    app.register_blueprint(stats)

    app.config.update(
        RECORD_EVENT=record_event,
        SHARED_DICT=shared_dict
    )

    return app

if __name__ == "__main__":
    manager = Manager()

    record_event = manager.Event()
    running_event = manager.Event()
    shared_dict = manager.dict()
    running_event.set()

    motion = MotionSensor(shared_data_dict=shared_dict, running_event=running_event)  # create a sensor process
    motion.setup()
    motion.start()

    app = create_app(record_event, shared_dict, debug=False)

    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        running_event.clear()
        motion.join()



