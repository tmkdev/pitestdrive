import logging
from flask import current_app, Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__, url_prefix='/', template_folder='templates')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@main.route('/')
def index():
    return render_template('main.html', 
                            datadict = current_app.config['SHARED_DICT'],
                            recording=current_app.config['RECORD_EVENT'],
                            cameradict = current_app.config['CAMERA_DICT'],
                            active='main')

@main.route('/record')
def record():
    current_app.config['RECORD_EVENT'].set()
    logging.warning('recording started')
    return redirect(url_for('main.index'))

@main.route('/stop')
def stop():
    current_app.config['RECORD_EVENT'].clear()
    logging.warning('recording stopped')
    return redirect(url_for('main.index'))

@main.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
