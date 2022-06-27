# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import abc
from typing import Type, List

from aqt import gui_hooks
from aqt.editor import EditorWebView, Editor
from aqt.qt import *
from aqt.utils import tooltip

from .helpers import config, default
from .mecab_controller import to_katakana, to_hiragana
from .reading import reading, reading_no_kanji


class ContextMenuAction(abc.ABC):
    subclasses: List[Type['ContextMenuAction']] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __init__(self, editor: Editor):
        self.editor = editor

    @classmethod
    def enabled(cls) -> bool:
        return config['context_menu'].get(cls.key, default['context_menu'][cls.key])

    @property
    @abc.abstractmethod
    def key(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def label(self) -> str:
        pass

    @abc.abstractmethod
    def action(self, text: str) -> str:
        pass

    def __call__(self, *args, **kwargs) -> None:
        if self.editor.currentField is not None and len(sel_text := self.editor.web.selectedText()) > 0:
            self.editor.doPaste(self.action(sel_text), internal=True, extended=False)
        else:
            tooltip("No text selected.")


class GenerateFurigana(ContextMenuAction):
    key = "generate_furigana"
    label = "Furigana for selection"
    action = staticmethod(reading)


class GenerateFuriganaNoKanji(ContextMenuAction):
    key = "generate_furigana_no_kanji"
    label = "Furigana without kanji for selection"
    action = staticmethod(reading_no_kanji)


class ToKatakana(ContextMenuAction):
    key = "to_katakana"
    label = "Convert to katakana"
    action = staticmethod(to_katakana)


class ToHiragana(ContextMenuAction):
    key = "to_hiragana"
    label = "Convert to hiragana"
    action = staticmethod(to_hiragana)


def add_context_menu_items(webview: EditorWebView, menu: QMenu) -> None:
    for Action in ContextMenuAction.subclasses:
        if Action.enabled():
            action = menu.addAction(Action.label)
            qconnect(action.triggered, Action(webview.editor))


def init():
    gui_hooks.editor_will_show_context_menu.append(add_context_menu_items)
