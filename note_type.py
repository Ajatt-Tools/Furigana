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

import os.path
from typing import Dict, Any

import anki.stdmodels
from anki.collection import Collection

NOTE_TYPE_NAME = "Japanese sentences"
FIELDS = [
    'SentKanji',
    'SentFurigana',
    'SentEng',
    'SentAudio',
    'MorphManFocus',
    'VocabKanji',
    'VocabFurigana',
    'VocabPitchPattern',
    'VocabPitchNum',
    'VocabDef',
    'VocabAudio',
    'Image',
    'Notes',
    'MakeProductionCard'
]
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "note_type")


def add_tsc_model(col: Collection) -> Dict[str, Any]:
    """Add TSCs note type to the add/clone note type screen"""
    note_type = col.models.new(NOTE_TYPE_NAME)
    for field in FIELDS:
        col.models.add_field(note_type, col.models.new_field(field))

    # css

    with open(os.path.join(TEMPLATE_DIR, 'japanese_sentences.css'), encoding='utf-8') as f:
        note_type['css'] = f.read()

    # recognition card

    rec_tmpl = col.models.new_template("Recognition")
    with open(os.path.join(TEMPLATE_DIR, 'recognition_front.html'), encoding='utf-8') as f:
        rec_tmpl['qfmt'] += f.read()
    with open(os.path.join(TEMPLATE_DIR, 'recognition_back.html'), encoding='utf-8') as f:
        rec_tmpl['afmt'] += f.read()
    col.models.addTemplate(note_type, rec_tmpl)

    # production card

    prod_tmpl = col.models.new_template("Production")
    with open(os.path.join(TEMPLATE_DIR, 'production_front.html'), encoding='utf-8') as f:
        prod_tmpl['qfmt'] += f.read()
    with open(os.path.join(TEMPLATE_DIR, 'production_back.html'), encoding='utf-8') as f:
        prod_tmpl['afmt'] += f.read()
    col.models.addTemplate(note_type, prod_tmpl)

    col.models.add(note_type)
    return note_type


def init():
    anki.stdmodels.models.append((NOTE_TYPE_NAME, add_tsc_model))
