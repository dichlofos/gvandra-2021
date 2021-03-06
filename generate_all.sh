#!/usr/bin/env bash
set -xe
python3 preprocess.py pandoc

pandoc report_gvandra_2021_pdf.md metadata.yaml \
    -V mainfont="Liberation Serif" \
    -V papersize="a4" \
    -V geometry="top=1cm" \
    -V geometry="left=1cm" \
    -V geometry="right=1cm" \
    -V geometry="bottom=2cm" \
    --pdf-engine=xelatex \
    -o report_gvandra_2021_pdf.pdf

pandoc report_gvandra_2021_ch.md metadata.yaml \
    -V mainfont="Liberation Serif" \
    -V papersize="a4" \
    -V geometry="top=1cm" \
    -V geometry="left=1cm" \
    -V geometry="right=1cm" \
    -V geometry="bottom=2cm" \
    --pdf-engine=xelatex \
    -o report_gvandra_2021_ch.pdf

if grep TODO report_gvandra_2021.md ; then
    echo "WARNING: Some TODOs not resolved yet"
fi