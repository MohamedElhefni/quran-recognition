import os
import datetime
import shutil
import glob
import requests
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, jsonify
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from utility import getSongName, init
from flask_sqlalchemy import SQLAlchemy
# from recognize import getSong
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='mohamed', password='mohamed**//', server='localhost', database='quran2')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
djv = init('config.json')
db = SQLAlchemy(app)
from models import Reader, Surah, Ayah

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['audio_data']
        if file:
            filename = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S") + ".mp3"
            RECORDS_PATH = join(dirname(realpath(__file__)), 'static/records/')
            file.save(os.path.join(RECORDS_PATH, filename))
            name = os.path.join(RECORDS_PATH, filename)
            songs = djv.recognize(FileRecognizer, name)
            os.remove(os.path.join(RECORDS_PATH, filename))
            return jsonify(songs)

    return render_template('index.html')


@app.route('/fingerprints', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        songs = request.files.getlist('audio')
        UPLOAD_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
        for song in songs:
            songDir = os.path.join(UPLOAD_PATH, song.filename)
            song.save(songDir)
            songName = getSongName(songDir)
            if songName:
                os.rename(os.path.join(UPLOAD_PATH, song.filename),
                          os.path.join(UPLOAD_PATH, songName))
        djv.fingerprint_directory(UPLOAD_PATH, ['.mp3'], 4)
        songs = glob.glob(UPLOAD_PATH + "*")
        for song in songs:
            os.remove(song)
    fingerprinted_songs = djv.get_fingerprinted_songs()
    return render_template('fingerprints.html', fingerprints=fingerprinted_songs)


@app.route('/readers')
def readers():
    # resp = requests.get(
    #     "http://api.alquran.cloud/v1/edition?format=audio&language=ar").json()
    readers = Reader.query.all()
    return render_template('readers.html', readers=readers)


@app.route('/reader/<id>')
def show(id):
    reader = Reader.query.filter_by(slug=id).first()
    return render_template('reader.html', reader=reader)


@app.route("/surah/<id>/<reader>")
def showSurah(id, reader):
    surah = Surah.query.filter_by(number=id).first()
    reader = Reader.query.filter_by(slug=reader).first()
    return render_template('surah.html', surah=surah, reader=reader)



import seed
