#!/usr/bin/env python3

import sys


def main():
    with open(sys.argv[1], encoding='utf-8') as f:
        first = True
        prev_day = None
        for line in f:
            if first:
                first = False
                continue

            line = line.strip()
            cols = [col.strip() for col in line.split('\t')]
            if len(cols) < 5:
                print('BAD', cols)

            photo_id = cols[0]
            day, in_day_id = photo_id.split('-')
            image_name = cols[1].replace(' ', '')
            # author = cols[2]
            # todo = cols[3]
            description = cols[4]

            if prev_day != day:
                # skip new line at next day
                prev_day = day
                print()

            md_line = '![](images/{image_name}.jpg "{description}")'.format(
                image_name=image_name,
                description=description,
            )
            print(md_line)

            # print(photo_id, image_name, description)


if __name__ == "__main__":
    main()
