from flask import current_app, Blueprint, render_template, request

hello = Blueprint('hello', __name__, url_prefix='/', template_folder='templates')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@hello.route('/')
def index():
    return render_template('hello.html', datadict = current_app.config['SHARED_DICT'])

@hello.route('/record')
def record():
    current_app.config['RECORD_EVENT'].set()
    return "Recording!!!"

@hello.route('/stop')
def stop():
    current_app.config['RECORD_EVENT'].clear()
    return "Stopped Recording!!!"


@hello.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
