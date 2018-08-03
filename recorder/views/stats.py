from flask import current_app, Blueprint, render_template

@stats.route('/')
def index():
    print(current_app.config['SHARED_DICT'])

    return render_template('stats.html', datadict = current_app.config['SHARED_DICT'])
