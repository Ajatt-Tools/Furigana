## AJT Furigana - config

*Anki needs to be restarted for changes to be applied.*

****

* `note_types`.
Tell the add-on what note types you use for Japanese.
By default, the add-on considers a note type Japanese
if it finds the text "japanese" in the note type's name.
Case is ignored.
* `fields`.
Pairs of fields to generate the reading for
and fields where the readings should be placed.
Default field names match the
[TSC](https://ankiweb.net/shared/info/1557722832)
note type.
* `furigana_suffix`.
If a field called "abc" exists, and another field called "abc
(furigana)" exists, they will be used as source and destination fields.
* `skip_numbers`.
Whether to add furigana to numbers or not.
* `skip_words`.
A comma-separated list of words that should be skipped when adding furigana.
* `generate_on_note_add`.
Automatically add readings to cards created by AnkiConnect with
[Yomichan](https://foosoft.net/projects/yomichan/).
* `toolbar`.
Controls additional buttons on the Anki Editor toolbar.
"Furigana" button lets you generate furigana in the selected field.
"Clean" button removes furigana in the selected field.
    * `enable`.
    Control whether a button is shown.
    * `shortcut`.
    Specify a keyboard shortcut for the button.
    * `text`.
    Customize the button's label.
* `context_menu`.
Toggles context menu actions.
You can enable or disable the following actions:
    * `generate_furigana`.
    Paste furigana for selection.
    * `to_katakana`.
    Convert selection to katakana.
    * `to_hiragana`.
    Convert selection to hiragana.

****

If you enjoy this add-on, please consider supporting my work by
**[pledging your support on Patreon](https://www.patreon.com/bePatron?u=43555128)**.
Thank you so much!
