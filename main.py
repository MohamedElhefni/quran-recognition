import os
import datetime
import sqlite3
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, url_for, redirect, jsonify
from recognize import getSong
app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        file = request.files['audio_data']
        if file:  
            filename = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S") + '.mp3'
            UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
            file.save(os.path.join(UPLOADS_PATH, filename))
            songStat = getSong(os.path.join(UPLOADS_PATH, filename))
            os.remove(os.path.join(UPLOADS_PATH, filename))
            return jsonify(songStat)
    return render_template('index.html')


