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

from typing import Sequence

from aqt import mw
from aqt.browser import Browser
from aqt.qt import *

from .misc import *
from .notetypes import is_supported_notetype
from .reading import mecab

ACTION_NAME = "Bulk-add furigana"


# Bulk updates
##########################################################################

def regenerate_readings(nids: Sequence):
    mw.checkpoint(ACTION_NAME)
    mw.progress.start()

    for nid in nids:
        note = mw.col.getNote(nid)
        if not is_supported_notetype(note):
            continue

        for src_field_name, dst_field_name in iter_fields():
            try:
                if (src_text := mw.col.media.strip(note[src_field_name]).strip()) and not note[dst_field_name]:
                    note[dst_field_name] = mecab.reading(src_text)
            except KeyError:
                continue

        note.flush()

    mw.progress.finish()
    mw.reset()


def setup_menu(browser: Browser):
    action = QAction(ACTION_NAME, browser)
    qconnect(action.triggered, lambda: regenerate_readings(browser.selectedNotes()))
    browser.form.menuEdit.addAction(action)


def init():
    if ANKI21_VERSION < 45:
        from anki.hooks import addHook
        addHook("browser.setupMenus", setup_menu)
    else:
        from aqt import gui_hooks

        gui_hooks.browser_menus_did_init.append(setup_menu)
