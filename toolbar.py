import re
from typing import List, Callable

from aqt import gui_hooks
from aqt.editor import Editor

from .helpers import config
from .reading import reading

RE_FLAGS = re.MULTILINE | re.IGNORECASE


def clean_furigana(expr: str) -> str:
    return re.sub(r'([^ ]+)\[[^ ]+]', r'\g<1>', expr, flags=RE_FLAGS).replace(' ', '')


def update_field(func: Callable):
    def decorator(editor: Editor):
        if (note := editor.note) and (field_n := editor.currentField) is not None:
            note.fields[field_n] = func(note.fields[field_n])
            editor.loadNoteKeepingFocus()

    return decorator


@update_field
def generate_furigana_in_field(expr: str) -> str:
    return reading(clean_furigana(expr))


@update_field
def clean_furigana_in_field(expr: str) -> str:
    return clean_furigana(expr)


def append_furigana_button(buttons: List[str], editor: Editor) -> None:
    but_cfg = config['toolbar']['furigana_button']
    b = editor.addButton(
        icon=None,
        cmd="generate_furigana_in_field",
        func=lambda _editor: generate_furigana_in_field(_editor),
        tip=f"Generate furigana in the field ({but_cfg['shortcut']})",
        keys=but_cfg['shortcut'],
        label=but_cfg['text'],
    )
    buttons.append(b)


def append_clean_furigana_button(buttons: List[str], editor: Editor) -> None:
    but_cfg = config['toolbar']['clean_furigana_button']
    b = editor.addButton(
        icon=None,
        cmd="clean_furigana_in_field",
        func=lambda _editor: clean_furigana_in_field(_editor),
        tip=f"Clean furigana in the field ({but_cfg['shortcut']})",
        keys=but_cfg['shortcut'],
        label=but_cfg['text'],
    )
    buttons.append(b)


def init():
    if config['toolbar']['furigana_button']['enable']:
        gui_hooks.editor_did_init_buttons.append(append_furigana_button)
    if config['toolbar']['clean_furigana_button']['enable']:
        gui_hooks.editor_did_init_buttons.append(append_clean_furigana_button)
