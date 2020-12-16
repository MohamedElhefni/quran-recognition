from main import db


reader_surah = db.Table('reader_surah', 
               db.Column('reader_id', db.Integer, db.ForeignKey('reader.id'), primary_key=True),
               db.Column('surah_id', db.Integer, db.ForeignKey('surah.id'), primary_key=True),
    )

class ReaderAyahs(db.Model):
    __tablename__ = "reader_ayah"
    id = db.Column(db.Integer, primary_key=True)
    reader_id = db.Column(db.Integer, db.ForeignKey(
        'reader.id'), primary_key=True)
    ayah_id = db.Column(db.Integer, db.ForeignKey(
        'ayah.id'), primary_key=True)
    isFingerprinted = db.Column(db.Boolean, default=False)
    reader = db.relationship("Reader", back_populates="ayahs")
    ayah = db.relationship("Ayah", back_populates="readers")


class Reader(db.Model):
    __tablename__ = 'reader'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    englishName = db.Column(db.String(100), unique=False, nullable=False)
    surahs = db.relationship("Surah", secondary=reader_surah)
    ayahs = db.relationship("ReaderAyahs", back_populates="reader")

    def __repr__(self):
        return f"Reader('{self.name}', '{self.englishName}')"


class Surah(db.Model):
    __tablename__ = 'surah'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String(30), unique=False, nullable=False)
    englishName = db.Column(db.String(50), unique=False, nullable=False)
    englishNameTranslation = db.Column(
        db.String(50), unique=False, nullable=False)
    revelationType = db.Column(db.String(10), unique=False, nullable=False)
    ayahs = db.relationship('Ayah', backref='surah', lazy=True)

    def __repr__(self):
        return f"Surah('{self.number}','{self.name}', '{self.englishName}', '{self.englishNameTranslation}', '{self.revelationType}')"


class Ayah(db.Model):
    __tablename__ = 'ayah'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    numberInSurah = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.Text, nullable=False)
    surah_id = db.Column(db.Integer, db.ForeignKey('surah.id'), nullable=False)
    readers = db.relationship("ReaderAyahs", back_populates="ayah")

    def __repr__(self):
        return f"Surah('{self.number}', '{self.text}')"
