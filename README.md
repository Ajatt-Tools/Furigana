# Japanese support

The purpose of this add-on is to automatically generate and bulk-generate furigana readings.
To do its job, the add-on relies on
[mecab_controller](https://github.com/Ajatt-Tools/mecab_controller).
Initially this add-on was forked from
[Japanese Support](https://ankiweb.net/shared/info/3918629684)
by Damien Elmes, but was almost completely rewritten.

The add-on comes with
[Japanese sentences](https://ankiweb.net/shared/info/1557722832)
note type optimized for usage with
[targeted sentence cards](https://tatsumoto-ren.github.io/blog/discussing-various-card-templates.html#targeted-sentence-cards-or-mpvacious-cards).

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
* **Note type**.
A new built-in note type designed for studying Japanese sentences.
You can find it by going to `Tools` > `Manage Note Types` > `Add` > `Japanese sentences`.
* **Compound words properly split.**
Words like `取って置き` or `言い方` produce correct furigana,
unlike the previous add-on.

## Caveats

Mecab is not perfect and sometimes generates incorrect readings.
There's nothing that can be done about it in a big picture,
so make sure you check the generated text and adjust it if necessary.
