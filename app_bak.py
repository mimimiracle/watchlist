import os
from flask import Flask, render_template, request, send_file, send_from_directory
from collections import OrderedDict

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def start():
    return 'hello'


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        f = request.files["file"]
        filename = os.path.join(BASE_PATH, "upload", f.filename)
        print(filename)
        f.save(filename)
        return "file upload successfully!"
    except Exception:
        return "failed!"


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    dir = os.path.join(BASE_PATH, 'download')
    return send_from_directory(dir, filename, as_attachment=True)


@app.route("/list", methods=["GET"])
def show_list():
    dir = os.path.join(BASE_PATH, 'download')
    file_list = os.listdir(dir)
    return OrderedDict(code=100, msg='success', data=file_list)


def mkdir(dirname):
    dir = os.path.join(BASE_PATH, dirname)
    if not os.path.exists(dir):
        os.makedirs(dir)


if __name__ == "__main__":
    mkdir('download')
    mkdir('upload')
    app.run(host='0.0.0.0', port=8000, debug=True)
