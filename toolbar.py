from typing import List

from aqt import gui_hooks
from aqt.editor import Editor

from .helpers import config
from .reading import reading


def replace_field_content(editor: Editor):
    if (note := editor.note) and (field_n := editor.currentField) is not None:
        note.fields[field_n] = reading(note.fields[field_n])
        editor.loadNoteKeepingFocus()


def append_editor_button(buttons: List[str], editor: Editor) -> None:
    shortcut = config.get('toolbar_button_shortcut')
    b = editor.addButton(
        icon=None,
        cmd="replace_with_furigana",
        func=lambda _editor: replace_field_content(_editor),
        tip=f"play sound ({shortcut})",
        keys=shortcut,
        label=config.get('toolbar_button_text')
    )
    buttons.append(b)


def init():
    if config.get('enable_toolbar_button'):
        gui_hooks.editor_did_init_buttons.append(append_editor_button)
