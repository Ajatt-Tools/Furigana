# -*- coding: utf-8 -*-

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

import re
from typing import List

from anki import hooks
from anki.notes import Note
from aqt import mw

from .mecab_controller import MecabController
from .misc import *
from .notetypes import is_supported_notetype


# Focus lost hook
##########################################################################

def find_dest_field_name(src_field_name: str) -> str:
    for src, dest in iter_fields():
        if src_field_name == src:
            return dest
    else:
        return src_field_name + config['furigana_suffix']


def on_focus_lost(changed: bool, note: Note, field_idx: int) -> bool:
    # japanese model?
    if not is_supported_notetype(note):
        return changed

    # have src and dst fields?
    src_field_name = note.keys()[field_idx]
    dest_field_name = find_dest_field_name(src_field_name)

    if not src_field_name or not dest_field_name:
        return changed

    # dst field exists?
    if dest_field_name not in note:
        return changed

    # dst field already filled?
    if note[dest_field_name]:
        return changed

    # grab source text
    if src_text := mw.col.media.strip(note[src_field_name]).strip():
        note[dest_field_name] = reading(src_text)
        return True

    return changed


# Note will flush hook
##########################################################################

def on_note_will_flush(note: Note) -> Note:
    if not config.get('generate_on_flush'):
        return note

    if mw.app.activeWindow():
        # only accept calls when add cards dialog or anki browser are not open.
        # otherwise this function conflicts with onFocusLost which is called on 'editFocusLost'
        return note

    # japanese model?
    if not is_supported_notetype(note):
        return note

    for src_field_name, dst_field_name in iter_fields():
        try:
            if (src_text := mw.col.media.strip(note[src_field_name]).strip()) and not note[dst_field_name]:
                note[dst_field_name] = reading(src_text)
        except KeyError:
            continue

    return note


# Reading
##########################################################################

mecab = MecabController()


def get_skip_words() -> List[str]:
    return re.split(r'[, ]+', config.get('skip_words', ''), flags=re.IGNORECASE)


def get_skip_numbers() -> List[str]:
    return list(NUMBERS) if config.get('skip_numbers') is True else []


def reading(expr: str) -> str:
    return mecab.reading(expr, get_skip_words() + get_skip_numbers())


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
    hooks.note_will_flush.append(on_note_will_flush)
