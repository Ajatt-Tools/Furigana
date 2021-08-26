# AJT Furigana

[![Rate on AnkiWeb](https://glutanimate.com/logos/ankiweb-rate.svg)](https://ankiweb.net/shared/info/1344485230)
[![Chat](https://img.shields.io/badge/chat-join-green)](https://tatsumoto-ren.github.io/blog/join-our-community.html)
[![Channel](https://shields.io/badge/channel-subscribe-blue?logo=telegram&color=3faee8)](https://t.me/ajatt_tools)
[![Patreon](https://img.shields.io/badge/patreon-support-orange)](https://www.patreon.com/bePatron?u=43555128)
![GitHub](https://img.shields.io/github/license/Ajatt-Tools/Furigana)

The purpose of this add-on is to automatically generate and bulk-generate furigana readings.
To do its job, the add-on relies on
[mecab_controller](https://github.com/Ajatt-Tools/mecab_controller).
The add-on comes with
[Japanese sentences](https://ankiweb.net/shared/info/1557722832)
note type optimized for usage with
[targeted sentence cards](https://tatsumoto-ren.github.io/blog/discussing-various-card-templates.html#targeted-sentence-cards-or-mpvacious-cards).

![demo](img/furigana_demo.webp)

## Features

* **Furigana.**
After you type in a word or phrase into the `SentKanji` or `VocabKanji` fields and hit `Tab`,
Anki will automatically generate furigana for you and place it in
`SentFurigana` and `VocabFurigana` fields respectfully.
Field names can be configured in settings.
* **Furigana on flush.**
Automatic furigana generation when a new note gets created with Yomichan.
* **Furigana from selection.**
You can convert any selected text to furigana by clicking `Furigana for selection`
in the context menu while using the note editor.
* **Bulk-add**.
To add furigana to multiple cards in bulk,
open the Anki Browser and press "Edit" > "Bulk-add furigana".
* **Toolbar button.**
You can replace the content of any selected field with furigana by pressing `振` on the toolbar.
* **Note type**.
A new built-in note type designed for studying Japanese sentences.
You can find it by going to `Tools` > `Manage Note Types` > `Add` > `Japanese sentences`.
* **Compound words properly split.**
Words like `取って置き` or `言い方` produce correct furigana,
unlike the previous add-on.

## Installation

Install from [AnkiWeb](https://ankiweb.net/shared/info/1344485230),
or manually with `git`:

```
git clone 'https://github.com/Ajatt-Tools/Furigana.git' ~/.local/share/Anki2/addons21/ajt_furigana
```

## Configuration

To configure the add-on, open the Anki Add-on Menu via "Tools" > "Add-ons" and select "AJT Furigana".
Then click the "Config" button on the right-side of the screen.

## Caveats

Mecab is not perfect and sometimes generates incorrect readings.
There's nothing that can be done about it in a big picture,
so make sure you check the generated text and adjust it if necessary.

## Acknowledgements

Initially this add-on was forked from
[Japanese Support](https://ankiweb.net/shared/info/3918629684)
by Damien Elmes, but was almost completely rewritten.
