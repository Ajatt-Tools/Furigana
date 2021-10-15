import abc
from typing import Dict, Type

from aqt import gui_hooks
from aqt.editor import EditorWebView, Editor
from aqt.qt import *
from aqt.utils import tooltip

from .helpers import config
from .mecab_controller import to_katakana, to_hiragana
from .reading import reading


class ContextMenuAction(metaclass=abc.ABCMeta):
    def __init__(self, editor: Editor):
        self.editor = editor

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
    label = "Furigana for selection"
    action = staticmethod(reading)


class ToKatakana(ContextMenuAction):
    label = "Convert to katakana"
    action = staticmethod(to_katakana)


class ToHiragana(ContextMenuAction):
    label = "Convert to hiragana"
    action = staticmethod(to_hiragana)


MENUS: Dict[str, Type[ContextMenuAction]] = {
    "generate_furigana": GenerateFurigana,
    "to_katakana": ToKatakana,
    "to_hiragana": ToHiragana,
}


def add_context_menu_items(webview: EditorWebView, menu: QMenu) -> None:
    for key, enabled in config['context_menu'].items():
        if enabled:
            action = menu.addAction(MENUS[key].label)
            qconnect(action.triggered, MENUS[key](webview.editor))


def init():
    gui_hooks.editor_will_show_context_menu.append(add_context_menu_items)
