import click
import requests
from tqdm import *
from flask.cli import with_appcontext
from main import app, db
from models import Reader, Surah, Ayah, ReaderSurahs

progress = tqdm


@click.command()
@with_appcontext
# def seed():
#     print("Seeding Started ... ")
#     print("Get Readers from api .. ")
#     readers = requests.get(
#         "http://api.alquran.cloud/v1/edition?format=audio&language=ar").json()['data']
#     for reader in progress(readers):
#         newReaer = Reader(
#             slug=reader['identifier'], name=reader['name'], englishName=reader['englishName'])
#         db.session.add(newReaer)
#         db.session.commit()
#         fullQuran = requests.get(f"http://api.alquran.cloud/v1/quran/{reader['identifier']}").json()['data']
#         for surah in fullQuran['surahs']:
#             newSurah = Surah(number=surah['number'], name=surah['name'], englishName=surah['englishName'],
#                              englishNameTranslation=surah['englishNameTranslation'], revelationType=surah['revelationType'], reader_id=newReaer.id)
#             db.session.add(newSurah)
#             db.session.commit()
#             ayahs = []
#             for ayah in progress(surah['ayahs']):
#                 newAyah = Ayah(
#                     number=ayah['number'], audio=ayah['audio'], text=ayah['text'], surah_id=newSurah.id)
#                 ayahs.append(newAyah)
#             db.session.add_all(ayahs)
#             db.session.commit()
def seed():
    db.create_all()
    print("Seeding Started ...")
    surahs = requests.get(
        "http://api.alquran.cloud/v1/quran/ar.abdulsamad").json()['data']['surahs']
    for surah in progress(surahs):
        newSurah = Surah(number=surah['number'], name=surah['name'], englishName=surah['englishName'],
                         englishNameTranslation=surah['englishNameTranslation'], revelationType=surah['revelationType'])
        db.session.add(newSurah)
        db.session.commit()
        ayahs = []
        for ayah in progress(surah['ayahs']):
            newAyah = Ayah(
                number=ayah['number'], text=ayah['text'], surah_id=newSurah.id)
            ayahs.append(newAyah)
        db.session.add_all(ayahs)
        db.session.commit()
    readers = requests.get(
        "http://api.alquran.cloud/v1/edition?format=audio&language=ar").json()['data']
    for reader in progress(readers):
    	newReader = Reader(
            slug=reader['identifier'], name=reader['name'], englishName=reader['englishName'])
    	for surah in Surah.query.all():
    		assoc = ReaderSurahs()
    		assoc.surah = surah
    		newReader.surahs.append(assoc)
    	db.session.add(newReader)
    	db.session.commit()

app.cli.add_command(seed)
# app.cli.add_command(seed2)
