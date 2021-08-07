from aqt import gui_hooks
from aqt.editor import EditorWebView, Editor
from aqt.qt import *
from aqt.utils import tooltip

from .reading import reading


def paste_furigana(editor: Editor) -> None:
    if editor.currentField is not None and len(sel_text := editor.web.selectedText()) > 0:
        editor.doPaste(reading(sel_text), internal=True, extended=False)
    else:
        tooltip("No text selected.")


def add_context_menu_item(webview: EditorWebView, menu: QMenu) -> None:
    action: QAction = menu.addAction("Furigana for selection")
    qconnect(action.triggered, lambda _=False: paste_furigana(webview.editor))


def init():
    gui_hooks.editor_will_show_context_menu.append(add_context_menu_item)
