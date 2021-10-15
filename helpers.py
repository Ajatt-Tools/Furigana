# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re
from typing import Iterator, Tuple

import aqt
from anki.notes import Note
from aqt import mw

ANKI21_VERSION = int(aqt.appVersion.split('.')[-1])
NUMBERS = "一二三四五六七八九十０１２３４５６７８９"
RE_FLAGS = re.MULTILINE | re.IGNORECASE


def get_config():
    return mw.addonManager.getConfig(__name__)


def clean_furigana(expr: str) -> str:
    return re.sub(r'([^ ]+)\[[^ ]+]', r'\g<1>', expr, flags=RE_FLAGS).replace(' ', '')


def iter_fields() -> Iterator[Tuple[str, str]]:
    for pair in config['fields']:
        yield pair['source'], pair['destination']


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


config = get_config()
