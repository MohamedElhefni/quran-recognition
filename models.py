from main import db


class ReaderSurahs(db.Model):
    __tablename__ = "surah_identifier"
    reader_id = db.Column(db.Integer, db.ForeignKey(
        'reader.id'), primary_key=True)
    surah_id = db.Column(db.Integer, db.ForeignKey(
        'surah.id'), primary_key=True)
    isFingerprinted = db.Column(db.Boolean, default=False)
    reader = db.relationship("Reader", back_populates="surahs")
    surah = db.relationship("Surah", back_populates="readers")


class Reader(db.Model):
    __tablename__ = 'reader'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)
    englishName = db.Column(db.String(100), unique=False, nullable=False)
    surahs = db.relationship("ReaderSurahs", back_populates="reader")

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
    readers = db.relationship("ReaderSurahs", back_populates="surah")

    def __repr__(self):
        return f"Surah('{self.number}','{self.name}', '{self.englishName}', '{self.englishNameTranslation}', '{self.revelationType}')"


class Ayah(db.Model):
    __tablename__ = 'ayah'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.Text, nullable=False)
    surah_id = db.Column(db.Integer, db.ForeignKey('surah.id'), nullable=False)

    def __repr__(self):
        return f"Surah('{self.number}', '{self.audio}', '{self.text}')"
