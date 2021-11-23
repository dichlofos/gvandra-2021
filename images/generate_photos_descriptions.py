#!/usr/bin/env python3

import re
import sys


def main():
    report_text = None
    with open("../report_gvandra_2021.md", encoding="utf-8") as f_r:
        report_text = f_r.read()

    def _flush_block(day, photo_block, report_text):
        begin = '<a name="photo_{}"></a>'.format(day)
        end = '<a name="photo_end_{}"></a>'.format(day)
        marker = begin + r'.*?' + end
        return re.sub(marker, begin + photo_block + end, report_text)

    with open(sys.argv[1], encoding='utf-8') as f:
        first = True
        prev_day = None

        photo_block = ""
        day = None

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
            if description[-1] == '.':
                # cut dots
                description = description[:-1]

            if prev_day != day:
                if photo_block:
                    new_report_text = _flush_block(day, photo_block, report_text)
                    assert new_report_text != report_text
                    report_text = new_report_text

                # skip new line at next day
                prev_day = day
                proper_in_day = 1
                print()

            if str(proper_in_day) != in_day_id:
                print("Inconsistent numbering at", photo_id)
                # sys.exit(1)

            md_line = (
                '<a name="{photo_id}"></a>\n'
                '![](images/{image_name}.jpg "Фото {photo_id}. {description}")\n'
                '<p style="text-align: center">{photo_id}. {description}</p>\n'
            ).format(
                photo_id=photo_id,
                image_name=image_name,
                description=description,
            )
            photo_block += md_line
            # print(md_line)

            proper_in_day += 1

        if photo_block:
            new_report_text = _flush_block(day, photo_block, report_text)
            assert new_report_text != report_text
            report_text = new_report_text


if __name__ == "__main__":
    main()
