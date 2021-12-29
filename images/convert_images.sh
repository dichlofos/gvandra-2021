#!/usr/bin/env bash
dir_name="reduced_85"
mkdir -p $dir_name
for i in *.jpg ; do
    width="$(convert $i -print "%w" /dev/null)"
    height="$(convert $i -print "%h" /dev/null)"

    output="$dir_name/$i"
    if (( $width > $height )) ; then
        # horizontal orientation
        convert -resize 1200x -quality 85 $i $output
    else
        # vertical orientation
        convert -resize x1200 -quality 85 $i $output
    fi
    input_size=$(stat -c '%s' $i)
    output_size=$(stat -c '%s' $output)

    printf "%30s %5d %5d %10d %10d\n" $i $width $height $input_size $output_size

done

