#!/usr/bin/env bash

readonly ROOT_DIR=$(git rev-parse --show-toplevel)
readonly BRANCH=$(git branch --show-current)
readonly ARCHIVE=japanese_support_$BRANCH.ankiaddon
readonly MANIFEST='manifest.json'

cd -- "$ROOT_DIR" || exit 1

export ROOT_DIR BRANCH

git archive HEAD --format=zip --output "$ARCHIVE"
# shellcheck disable=SC2016
git submodule foreach 'git archive HEAD --prefix=$path/ --format=zip --output "$ROOT_DIR/${path}_${BRANCH}.zip"'
zipmerge "$ARCHIVE" ./*.zip
rm -- ./*.zip

if [[ $* ]]; then
    # https://addon-docs.ankiweb.net/#/sharing?id=sharing-outside-ankiweb
    # If you wish to distribute .ankiaddon files outside of AnkiWeb,
    # your add-on folder needs to contain a ‘manifest.json’ file.
    {
        echo '{'
        echo -e "\t\"package\": \"ajt_japanese_support\","
        echo -e "\t\"name\": \"AJT Japanese support\","
        echo -e "\t\"mod\": $(date -u '+%s')"
        echo '}'
    } > "$MANIFEST"
    zip -u "$ARCHIVE" "$MANIFEST"
    rm -- "$MANIFEST"
fi
