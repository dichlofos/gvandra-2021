#!/usr/bin/env python3

import re
import sys


_PHOTOS_DESC_NAME = "images.tsv"
_REPORT_NAME = "../source_report_gvandra_2021.md"
_OUTPUT_REPORT_NAME = "../report_gvandra_2021.md"


def _flush_block(day, photo_block, report_text):
    begin = '<a name="photo_{}"></a>'.format(day)
    end = '<a name="photo_end_{}"></a>'.format(day)
    marker = begin + r'.*?' + end
    print(marker)
    return re.sub(marker, begin + '\n' + photo_block + end, report_text, flags=re.DOTALL)


def _read_file(file_name):
    text = None
    with open(file_name, encoding="utf-8") as f:
        text = f.read()
    return text


def main():
    source_report_text = _read_file(_REPORT_NAME)
    assert source_report_text

    report_text = source_report_text

    photos = {}
    photos_by_day = {}

    with open(_PHOTOS_DESC_NAME, encoding='utf-8') as f:
        first = True
        prev_day = None

        photo_block = ""
        day = None
        proper_in_day = 1

        for line in f:
            if first:
                print('SKIPPED:', line)
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

            assert proper_in_day is not None and proper_in_day > 0 and proper_in_day < 30

            photo = {
                "day": day,
                "in_day": proper_in_day,
                "image_name": image_name,
                "description": description,
            }
            photos[image_name] = photo

            if day not in photos_by_day:
                photos_by_day[day] = []

            photos_by_day[day].append(photo)

            if prev_day != day:
                # skip new line at next day
                prev_day = day
                proper_in_day = 1
                print()

            print('{:3}   {:3}   {:30}   {}'.format(day, proper_in_day, image_name, description))

            if str(proper_in_day) != in_day_id:
                # print("Inconsistent numbering at", photo_id)
                # sys.exit(1)
                pass

            proper_in_day += 1

    print("Photos loaded:", len(photos))

    # first, replace photo marks by days
    for day in photos_by_day:
        day_photos = photos_by_day[day]
        photo_block = ""
        for photo in day_photos:
            photo_id = "{}-{}".format(day, photo["in_day"])
            md_line = (
                '<a name="{photo_id}"></a>\n'
                '![](images/{image_name}.jpg "Фото {photo_id}. {description}")\n'
                '<p style="text-align: center">{photo_id}. {description}</p>\n\n'
            ).format(
                photo_id=photo_id,
                image_name=photo["image_name"],
                description=photo["description"],
            )
            photo_block += md_line

        print("Replacing block in day", day)
        new_report_text = _flush_block(day, photo_block, report_text)

        assert new_report_text != report_text  # check replacement is really done
        report_text = new_report_text

    sys.exit(0)

    with open(_PHOTOS_DESC_NAME, encoding='utf-8') as f:
        first = True
        prev_day = None
        photo = {}

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
                    new_report_text = _flush_block(prev_day, photo_block, report_text)
                    print(prev_day)
                    assert new_report_text != report_text
                    report_text = new_report_text
                    photo_block = ''

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
                '<p style="text-align: center">{photo_id}. {description}</p>\n\n'
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
            # print(day)
            assert new_report_text != report_text
            report_text = new_report_text

    # print(report_text)

    with open(_REPORT_NAME, 'w', encoding='utf-8') as f:
        f.write(report_text)


if __name__ == "__main__":
    main()
