from flask import Blueprint, render_template, url_for, request
from app.models.panda import *
from app.models.firebase import *



prefix = 'upload'

bp = Blueprint(
    prefix,
    __name__,
    url_prefix='/' + prefix
)


@bp.route('/', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')


@bp.route('/table/', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        file = request.files['file']
        draw_table = pandas_processing(file)
        firebase_push('actual', get_last_upload())
        return render_template('table.html',
                                table=draw_table,
                               )


@bp.route('/table-dummy/', methods=['GET'])
def table_dummy():
    file = 'app/static/dummy.csv'
    draw_table = pandas_processing(file)
    firebase_push('dummy', get_last_upload())
    return render_template('table.html',
                            table=draw_table,
                           )
