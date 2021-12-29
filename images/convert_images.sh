#!/usr/bin/env bash
dir_name="reduced_85"
mkdir -p $dir_name
for i in *.jpg ; do
    echo $i
    convert -resize 2400x1800 -quality 90 $i $dir_name/$i
done

