import os
import datetime
import shutil
import glob
from os.path import join, dirname, realpath
from flask import Flask, render_template, request,   jsonify
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from utility import getSongName, init

# from recognize import getSong
app = Flask(__name__)
djv = init('config.json')


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
