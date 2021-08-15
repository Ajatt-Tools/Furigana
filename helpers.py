from typing import Iterator, Tuple

import aqt
from anki.notes import Note

ANKI21_VERSION = int(aqt.appVersion.split('.')[-1])
NUMBERS = "一二三四五六七八九十０１２３４５６７８９"
config = aqt.mw.addonManager.getConfig(__name__)


def iter_fields() -> Iterator[Tuple[str, str]]:
    return zip(config['source_fields'], config['destination_fields'])


def get_notetype(note: Note) -> dict:
    if hasattr(note, 'note_type'):
        return note.note_type()
    else:
        return note.model()


def is_supported_notetype(note: Note) -> bool:
    # Check if this is a supported note type.

    if not config["note_types"]:
        # supported note types weren't specified by the user.
        # treat all note types as supported
        return True

    this_notetype = get_notetype(note)['name']
    return any(notetype.lower() in this_notetype.lower() for notetype in config["note_types"])
