from flask import Flask, render_template


app = Flask(__name__, template_folder='dist')


@app.route('/', methods=['GET'])
def index():
    return '¯\_(ツ)_/¯'


from app import upload
app.register_blueprint(upload.bp)
