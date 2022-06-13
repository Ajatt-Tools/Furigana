# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from dataclasses import dataclass
from typing import List, Callable

from aqt import gui_hooks
from aqt.editor import Editor

from .helpers import *
from .reading import reading, reading_no_kanji


def get_default_config():
    manager = aqt.mw.addonManager
    addon = manager.addonFromModule(__name__)
    return manager.addonConfigDefaults(addon)


@dataclass(frozen=True)
class BtnCfg:
    id: str
    on_press: Callable[[str], str]
    tip: str
    __default = get_default_config()

    def __get(self, button_id: str):
        return config['toolbar'].get(button_id, self.__default['toolbar'][button_id])

    @property
    def enabled(self) -> bool:
        return self.__get(self.id)['enable']

    @property
    def shortcut(self) -> str:
        return self.__get(self.id)['shortcut']

    @property
    def text(self) -> str:
        return self.__get(self.id)['text']


def on_button_press(func: Callable):
    def decorator(editor: Editor) -> None:
        if (note := editor.note) and (field_n := editor.currentField) is not None:
            note.fields[field_n] = func(note.fields[field_n])
            editor.loadNoteKeepingFocus()

    return decorator


def create_callback(cfg: BtnCfg):
    def make_toolbar_button(buttons: List[str], editor: Editor) -> None:
        b = editor.addButton(
            icon=None,
            cmd=cfg.id,
            func=on_button_press(cfg.on_press),
            tip=f"{cfg.tip} ({cfg.shortcut})",
            keys=cfg.shortcut,
            label=cfg.text,
        )
        buttons.append(b)

    return make_toolbar_button


def init():
    buttons = (
        BtnCfg(
            id='furigana_button',
            on_press=lambda expr: reading(clean_furigana(expr)),
            tip='Generate furigana in the field',
        ),
        BtnCfg(
            id='clean_furigana_button',
            on_press=clean_furigana,
            tip='Clean furigana in the field',
        ),
        BtnCfg(
            id='furigana_no_kanji_button',
            on_press=lambda expr: reading_no_kanji(clean_furigana(expr)),
            tip='Generate furigana without kanji in the field'
        )
    )
    for cfg in buttons:
        if cfg.enabled:
            gui_hooks.editor_did_init_buttons.append(create_callback(cfg))
