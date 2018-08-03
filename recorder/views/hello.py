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

@hello.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'