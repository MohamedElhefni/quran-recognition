import click
import requests
from tqdm import *
from flask.cli import with_appcontext
from main import app, db
from models import Reader, Surah, Ayah, ReaderAyahs

progress = tqdm


def seedFullQuran():
    surahs = requests.get(
        "http://api.alquran.cloud/v1/quran/ar.abdulsamad").json()
    if surahs['code'] == 200:
        for surah in progress(surahs['data']['surahs']):
            newSurah = Surah(number=surah['number'], name=surah['name'], englishName=surah['englishName'],
                             englishNameTranslation=surah['englishNameTranslation'], revelationType=surah['revelationType'])
            db.session.add(newSurah)
            db.session.commit()
            ayahs = []
            for ayah in progress(surah['ayahs']):
                newAyah = Ayah(
                    number=ayah['number'], numberInSurah=ayah['numberInSurah'], text=ayah['text'], surah_id=newSurah.id)
                ayahs.append(newAyah)
            db.session.add_all(ayahs)
            db.session.commit()
    else:
        print(surahs['data'])
        exit()


def seedReadersAndReaderAyahsRelation():
    readers = requests.get(
        "http://api.alquran.cloud/v1/edition?format=audio&language=ar").json()['data']
    for reader in progress(readers):
        newReader = Reader(
            slug=reader['identifier'], name=reader['name'], englishName=reader['englishName'])
        for ayah in Ayah.query.all():
            asoc = ReaderAyahs()
            asoc.ayah = ayah
            newReader.ayahs.append(asoc)
        db.session.add(newReader)
        db.session.commit()


def seedReaderSurahsRelation():
    for reader in progress(Reader.query.all()):
        for surah in Surah.query.all():
            reader.surahs.append(surah)
        db.session.add(reader)
        db.session.commit()


@click.command()
@with_appcontext
def seed():
    db.create_all()
    print("Seeding Started ...")
    print("Seeding Full Quran ...")
    seedFullQuran()
    print("Seeding Readers Ayahs Relationship")
    seedReadersAndReaderAyahsRelation()
    print("Seeding Readers Surah RelationShip")
    seedReaderSurahsRelation()


app.cli.add_command(seed)
