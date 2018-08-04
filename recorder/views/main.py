from flask import current_app, Blueprint, render_template, request

main = Blueprint('main', __name__, url_prefix='/', template_folder='templates')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@main.route('/')
def index():
    return render_template('hello.html', datadict = current_app.config['SHARED_DICT'])

@main.route('/record')
def record():
    current_app.config['RECORD_EVENT'].set()
    return "Recording!!!"

@main.route('/stop')
def record():
    current_app.config['RECORD_EVENT'].clear()
    return "Stopped Recording!!!"


@main.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'