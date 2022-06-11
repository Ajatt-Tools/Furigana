# Japanese support add-on for Anki 2.1
# Copyright (C) 2021  Ren Tatsumoto. <tatsu at autistici.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Any modifications to this file must keep this entire header intact.

from typing import List

import anki.collection
from anki.hooks import wrap
from anki.utils import htmlToTextLine

from .helpers import *
from .mecab_controller import MecabController, to_hiragana, format_output
from .tokens import tokenize, ParseableToken


# Focus lost hook
##########################################################################

def find_dest_field_name(src_field_name: str) -> str:
    for src, dest in iter_fields():
        if src_field_name == src:
            return dest
    else:
        return src_field_name + config['furigana_suffix']


def can_fill_destination(note: Note, src_field: str, dst_field: str) -> bool:
    # Field names are empty or None
    if not src_field or not dst_field:
        return False

    # The note doesn't have fields with these names
    if src_field not in note or dst_field not in note:
        return False

    # Field is empty
    if len(htmlToTextLine(note[dst_field])) == 0:
        return True

    return False


def fill_destination(note: Note, src_field: str, dst_field: str) -> bool:
    if not can_fill_destination(note, src_field, dst_field):
        return False

    # grab source text and update note
    if src_text := mw.col.media.strip(note[src_field]).strip():
        if config.get('skip_kanji'): 
            note[dst_field] = reading_no_kanji(src_text)
        else:
            note[dst_field] = reading(src_text)
        return True

    return False


def on_focus_lost(changed: bool, note: Note, field_idx: int) -> bool:
    # This notetype name is not included in the config file
    if not is_supported_notetype(note):
        return changed

    src_field = note.keys()[field_idx]
    dst_field = find_dest_field_name(src_field)

    return True if fill_destination(note, src_field, dst_field) else changed


# Note add hook
##########################################################################

def should_add_furigana(note: Note) -> bool:
    return all((
        config.get('generate_on_note_add') is True,
        mw.app.activeWindow() is None,
        note.id == 0,
        is_supported_notetype(note),
    ))


def on_add_note(_col, note: Note, _did) -> None:
    if not should_add_furigana(note):
        return

    for src_field, dst_field in iter_fields():
        fill_destination(note, src_field, dst_field)


# Reading
##########################################################################


def get_skip_words() -> List[str]:
    return re.split(r'[, ]+', config.get('skip_words', ''), flags=re.IGNORECASE)


def get_skip_numbers() -> List[str]:
    return list(NUMBERS) if config.get('skip_numbers') is True else []


def reading(src_text: str) -> str:
    skip_words = get_skip_words() + get_skip_numbers()
    substrings = []
    for token in tokenize(src_text):
        if isinstance(token, ParseableToken):
            for out in mecab.translate(token):
                substrings.append(
                    format_output(out.word, out.hiragana_reading)
                    if out.katakana_reading and out.word not in skip_words and out.headword not in skip_words
                    else out.word
                )
        else:
            substrings.append(token)

    return ''.join(substrings).strip()

def reading_no_kanji(src_text: str) -> str:
    skip_words = get_skip_words() + get_skip_numbers()
    substrings = []
    for token in tokenize(src_text):
        if isinstance(token, ParseableToken):
            for out in mecab.translate(token):
                substrings.append(
                    out.hiragana_reading
                    if out.katakana_reading and out.word not in skip_words and out.headword not in skip_words
                    else out.word
                )
        else:
            substrings.append(token)

    return ''.join(substrings).strip()

mecab = MecabController(verbose=True)


# Init
##########################################################################

def init():
    if ANKI21_VERSION < 45:
        from anki.hooks import addHook

        addHook('editFocusLost', on_focus_lost)
    else:
        from aqt import gui_hooks

        gui_hooks.editor_did_unfocus_field.append(on_focus_lost)

    # Generate when AnkiConnect adds a new note
    anki.collection.Collection.add_note = wrap(anki.collection.Collection.add_note, on_add_note, 'before')
