#!/usr/bin/env bash
set -xe
pandoc test.md \
    -V mainfont="Liberation Serif" \
    -V papersize="a4" \
    -V geometry="top=1cm" \
    -V geometry="left=1cm" \
    -V geometry="right=1cm" \
    -V geometry="bottom=2cm" \
    --pdf-engine=xelatex \
    -o test.pdf
