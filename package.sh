#!/usr/bin/env bash

readonly ROOT_DIR=$(git rev-parse --show-toplevel)
readonly BRANCH=$(git branch --show-current)
readonly ARCHIVE=ajt_furigana_${BRANCH}.ankiaddon

cd -- "$ROOT_DIR" || exit 1

export ROOT_DIR BRANCH

git archive HEAD --format=zip --output "$ARCHIVE"
# shellcheck disable=SC2016
git submodule foreach 'git archive HEAD --prefix=$path/ --format=zip --output "$ROOT_DIR/${path}_${BRANCH}.zip"'
zipmerge "$ARCHIVE" ./*.zip
rm -- ./*.zip
