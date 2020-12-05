import mutagen
import json
import sys
from mutagen.easyid3 import EasyID3
from dejavu import Dejavu


def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)


def getSongName(songDir):
    try:
        songName = EasyID3(songDir)
        fullName = songName['artist'][0] + "-" + songName['title'][0] + ".mp3" if len(songName) > 1 else ''
    except mutagen.id3.ID3NoHeaderError:
        fullName = ''
    return fullName
