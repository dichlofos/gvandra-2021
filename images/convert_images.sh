#!/usr/bin/env bash
mkdir -p reduced
for i in *.jpg ; do
    convert -width 1200 $i reduced/$i
done

