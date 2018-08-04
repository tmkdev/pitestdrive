import logging
import os
from flask import current_app, Blueprint, render_template, request, redirect, url_for, send_from_directory


files = Blueprint('files', __name__, url_prefix='/files', template_folder='templates')

@files.route('/')
def index():
    fpath='/home/pi/tracklogs'

    flist = sorted(os.listdir(fpath))
    stats = [os.stat(os.path.join(fpath, x)) for x in flist]

    listing = dict(zip(flist, stats))

    return render_template('files.html', listing=listing, active='files')

@files.route('/download/<string:filename>')
def download(filename):
    fpath='/home/pi/tracklogs'

    return send_from_directory(fpath, filename)

@files.route('/delete/<string:filename>')
def delete(filename):
    fpath='/home/pi/tracklogs'

    os.unlink(os.path.join(fpath, filename))

    return redirect(url_for('files.index'))
