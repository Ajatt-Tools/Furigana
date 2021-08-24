import re
from typing import List

from aqt import gui_hooks
from aqt.editor import Editor

from .helpers import config
from .reading import reading


def clean_furigana(expr: str) -> str:
    return re.sub(r'([^ ]+)\[[^ ]+]', r'\g<1>', expr, re.MULTILINE | re.IGNORECASE)


def replace_field_content(editor: Editor):
    if (note := editor.note) and (field_n := editor.currentField) is not None:
        note.fields[field_n] = reading(clean_furigana(note.fields[field_n]))
        editor.loadNoteKeepingFocus()


def append_editor_button(buttons: List[str], editor: Editor) -> None:
    shortcut = config['toolbar']['furigana_button_shortcut']
    b = editor.addButton(
        icon=None,
        cmd="replace_with_furigana",
        func=lambda _editor: replace_field_content(_editor),
        tip=f"Generate furigana for the field ({shortcut})",
        keys=shortcut,
        label=config['toolbar']['furigana_button_text']
    )
    buttons.append(b)


def init():
    if config['toolbar']['furigana_button_enable']:
        gui_hooks.editor_did_init_buttons.append(append_editor_button)
