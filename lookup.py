# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Dictionary lookup support.
#

import re
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo

# Backwards compatibility
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+
try:
    setUrl = QUrl.setEncodedUrl # Python 2.X
except AttributeError:
    setUrl = QUrl.setUrl # Python 3+

class Lookup(object):

    def __init__(self):
        pass

    def selection(self, function):
        "Get the selected text and look it up with FUNCTION."
        text = mw.web.selectedText()
        text = text.strip()
        if not text:
            showInfo(("Empty selection."))
            return
        if "\n" in text:
            showInfo(("Can't look up a selection with a newline."))
            return
        function(text)

    def edictKanji(self, text):
        self.edict(text, True)

    def edict(self, text, kanji=False):
        "Look up TEXT with edict."
        if kanji:
            x="M"
        else:
            x="U"
        baseUrl="http://nihongo.monash.edu/cgi-bin/wwwjdic?1M" + x
        if self.isJapaneseText(text):
            baseUrl += "J"
        else:
            baseUrl += "E"
        url = baseUrl + quote(text.encode("utf-8"))
        qurl = QUrl()
        setUrl(qurl, url)
        QDesktopServices.openUrl(qurl)

    def jishoKanji(self, text):
        self.jisho(text, True)

    def jisho(self, text, kanji=False):
        "Look up TEXT with jisho."
        if kanji:
            baseUrl="http://jisho.org/kanji/details/"
        else:
            baseUrl="http://jisho.org/words?"
            if self.isJapaneseText(text):
                baseUrl+="jap="
            else:
                baseUrl+="eng="
        url = baseUrl + quote(text.encode("utf-8"))
        qurl = QUrl()
        setUrl(qurl, url)
        QDesktopServices.openUrl(qurl)

    def alc(self, text):
        "Look up TEXT with ALC."
        newText = quote(text.encode("utf-8"))
        url = (
            "http://eow.alc.co.jp/" +
            newText +
            "/UTF-8/?ref=sa")
        qurl = QUrl()
        setUrl(qurl, url)
        QDesktopServices.openUrl(qurl)

    def isJapaneseText(self, text):
        "True if 70% of text is a Japanese character."
        total = len(text)
        if total == 0:
            return True
        jp = 0
        en = 0
        for c in text:
            if ord(c) >= 0x2E00 and ord(c) <= 0x9FFF:
                jp += 1
            if re.match("[A-Za-z]", c):
                en += 1
        if not jp:
            return False
        return ((jp + 1) / float(en + 1)) >= 1.0

def initLookup():
    if not getattr(mw, "lookup", None):
        mw.lookup = Lookup()

def _field(name):
    try:
        return mw.reviewer.card.note()[name]
    except:
        return

def onLookupExpression(name="Expression"):
    initLookup()
    txt = _field(name)
    if not txt:
        return showInfo("No %s in current note." % name)
    mw.lookup.alc(txt)

def onLookupMeaning():
    onLookupExpression("Meaning")

def onLookupEdictSelection():
    initLookup()
    mw.lookup.selection(mw.lookup.edict)

def onLookupEdictKanjiSelection():
    initLookup()
    mw.lookup.selection(mw.lookup.edictKanji)

def onLookupJishoSelection():
    initLookup()
    mw.lookup.selection(mw.lookup.jisho)

def onLookupJishoKanjiSelection():
    initLookup()
    mw.lookup.selection(mw.lookup.jishoKanji)

def onLookupAlcSelection():
    initLookup()
    mw.lookup.selection(mw.lookup.alc)

def createMenu():
    # pylint: disable=unnecessary-lambda
    ml = QMenu()
    ml.setTitle("Lookup")
    mw.form.menuTools.addAction(ml.menuAction())
    # make it easier for other plugins to add to the menu
    mw.form.menuLookup = ml
    # add actions
    a = QAction(mw)
    a.setText("...expression on alc")
    a.setShortcut("Ctrl+Shift+1")
    ml.addAction(a)
    # Call from lambda to preserve default argument
    a.triggered.connect(lambda: onLookupExpression())
    a = QAction(mw)
    a.setText("...meaning on alc")
    a.setShortcut("Ctrl+Shift+2")
    ml.addAction(a)
    a.triggered.connect(onLookupMeaning)
    a = QAction(mw)
    a.setText("...selection on alc")
    a.setShortcut("Ctrl+Shift+3")
    ml.addAction(a)
    ml.addSeparator()
    a.triggered.connect(onLookupAlcSelection)
    a = QAction(mw)
    a.setText("...word selection on edict")
    a.setShortcut("Ctrl+Shift+4")
    ml.addAction(a)
    a.triggered.connect(onLookupEdictSelection)
    a = QAction(mw)
    a.setText("...kanji selection on edict")
    a.setShortcut("Ctrl+Shift+5")
    ml.addAction(a)
    a.triggered.connect(onLookupEdictKanjiSelection)
    ml.addSeparator()
    a = QAction(mw)
    a.setText("...word selection on jisho")
    a.setShortcut("Ctrl+Shift+6")
    ml.addAction(a)
    a.triggered.connect(onLookupJishoSelection)
    a = QAction(mw)
    a.setText("...kanji selection on jisho")
    a.setShortcut("Ctrl+Shift+7")
    ml.addAction(a)
    a.triggered.connect(onLookupJishoKanjiSelection)

# def disableMenu():
#     mw.mainWin.menuLookup.setEnabled(False)

# def enableMenu():
#     mw.mainWin.menuLookup.setEnabled(True)

# addHook('disableCardMenuItems', disableMenu)
# addHook('enableCardMenuItems', enableMenu)

createMenu()
