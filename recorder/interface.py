import time
from flask import Flask
from multiprocessing import Process, Manager

from views.hello import hello
from views.stats import stats

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
    shared_dict = manager.dict()

    shared_dict = { 'xl': 12.3, 'yl': 3.4 }
    app = create_app(record_event, shared_dict, debug=False)
    
    try:
        app.run()
    except KeyboardInterrupt:        
        pass
