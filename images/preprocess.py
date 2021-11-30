#!/usr/bin/env python3

import re


_PHOTOS_DESC_NAME = "images.tsv"
_REPORT_NAME = "../source_report_gvandra_2021.md"
_OUTPUT_REPORT_NAME = "../report_gvandra_2021.md"


def _flush_block(day, photo_block, report_text):
    begin = '<a name="photo_{}"></a>'.format(day)
    end = '<a name="photo_end_{}"></a>'.format(day)
    marker = begin + r'.*?' + end
    # print(marker)
    return re.sub(marker, begin + '\n' + photo_block + end, report_text, flags=re.DOTALL)


def _read_file(file_name):
    text = None
    with open(file_name, encoding="utf-8") as f:
        text = f.read()
    return text


_TEST_TEXT = (
    """GPS), примеченном в походе 2019 года. От Ворошиловских кошей до места ночевки дошли за 1 час 7 минут ЧХВ.

<a name="photo_1"></a>
<a name="1-1"></a>
![](images/DSCF3954.jpg "Фото 1-1. Начало маршрута у погранзаставы Хурзук")
<p style="text-align: center">1-1. Начало маршрута у погранзаставы Хурзук</p>

<a name="1-2"></a>
![](images/DSCF3984.jpg "Фото 1-2. Характер дороги в д.р. Кубань")
<p style="text-align: center">1-2. Характер дороги в д.р. Кубань</p>

<a name="1-3"></a>
![](images/DSCF3966.jpg "Фото 1-3. Каньон р. Кубань")
<p style="text-align: center">1-3. Каньон р. Кубань</p>

<a name="1-4"></a>
![](images/DSCF3994.jpg "Фото 1-4. Характер дороги в д.р. Кубань")
<p style="text-align: center">1-4. Характер дороги в д.р. Кубань</p>

<a name="1-5"></a>
![](images/DSCF4032.jpg "Фото 1-5. Мост через р. Акбаши и место обеда")
<p style="text-align: center">1-5. Мост через р. Акбаши и место обеда</p>

<a name="1-6"></a>
![](images/DSCF4155-Pano.jpg "Фото 1-6. Место стоянки в д.р. Уллу-Езень")
<p style="text-align: center">1-6. Место стоянки в д.р. Уллу-Езень</p>

<a name="photo_end_1"></a>

### День 2. 20 августа 2021 года
*м.н. – д.р. Уллу-Езень - лед. Хасанкой-Сюрюлген - пер. Кичкинекол В. (Сварщиков) (1А) – д. притока р. Кичкинекол*""")


def main():
    replace_result = _flush_block("1", "REPLACEMENT", _TEST_TEXT)
    assert replace_result != _TEST_TEXT

    source_report_text = _read_file(_REPORT_NAME)
    assert source_report_text

    # regex test
    assert _TEST_TEXT in source_report_text

    # fix times in tables
    source_lines = source_report_text.split('\n')
    fixed_source_lines = []
    for line in source_lines:
        if '|' in line:
            new_line = re.sub(r'([0-9]+)ч ([0-9]+)м', r'\1:\2', line)
            if line != new_line:
                print("Fixed times in:", new_line)
                line = new_line
        fixed_source_lines.append(line)
    new_source_report_text = '\n'.join(fixed_source_lines)
    if source_report_text != new_source_report_text:
        # write fixed source
        print("Source fixed, writing output to", _REPORT_NAME)
        with open(_REPORT_NAME, 'w', encoding='utf-8') as f:
            f.write(new_source_report_text)
        source_report_text = new_source_report_text

    report_text = source_report_text
    # report_text =  _TEST_TEXT
    report_text = report_text.replace('\r', '')
    # report_text = report_text.replace('\n', '__WRAP__')

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
                '<a name="ph_{photo_id}"></a>\n'
                '![](images/reduced/{image_name}.jpg "Фото {photo_id}. {description}")\n'
                '<p style="text-align: center;">{photo_id}. {description}</p>\n\n'
            ).format(
                photo_id=photo_id,
                image_name=photo["image_name"],
                description=photo["description"],
            )
            photo_block += md_line

        print("Replacing block in day", day)
        new_report_text = _flush_block(day, photo_block, report_text)

        # print(new_report_text)
        # print("OLD:")
        # print(report_text)
        assert new_report_text != report_text  # check replacement is really done
        report_text = new_report_text

    for image_name in photos:
        photo = photos[image_name]
        day = photo["day"]
        photo_id = "{}-{}".format(day, photo["in_day"])
        print("Replacing ", image_name)
        new_report_text = report_text.replace(
            "PHOTO:{}".format(image_name),
            "[Фото {photo_id}](#ph_{photo_id})".format(photo_id=photo_id),
        )
        assert new_report_text != report_text
        report_text = new_report_text

    # write output
    with open(_OUTPUT_REPORT_NAME, 'w', encoding='utf-8') as f:
        f.write(new_report_text)

    print("Output written to ", _OUTPUT_REPORT_NAME)


if __name__ == "__main__":
    main()
