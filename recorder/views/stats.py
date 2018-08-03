from flask import current_app, Blueprint, render_template

stats = Blueprint('stats', __name__, url_prefix='/stats', template_folder='templates')

@stats.route('/')
def index():
    return render_template('stats.html', datadict = current_app.config['SHARED_DICT'])
