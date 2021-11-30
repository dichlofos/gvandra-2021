#!/usr/bin/env bash
dir_name="sample_1600"
mkdir -p $dir_name
for i in *.jpg ; do
    echo $i
    convert -resize 1600x1200 -quality 93 $i $dir_name/$i
done

