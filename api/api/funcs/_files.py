"""
Files functionality for the API
"""

import os
import re
import base64
import string
import random
import json

import requests
from PIL import Image, ExifTags


with open('sets.json', 'r') as file:
    sets = json.loads(file.read())
    SIDE_OPTIMIZED = sets['side_optimized']


def get_file(url, num):
    """ Check existence the file by name """

    for i in os.listdir('../data/load/{}/'.format(url)):
        if re.search(rf"^{str(num)}.", i):
            return i

    return None

def max_image(url):
    """ Next image ID """

    files = os.listdir(url)
    k = 0
    for i in files:
        j = re.findall(r'\d+', i)
        if len(j) and int(j[0]) > k:
            k = int(j[0])
    return k+1

def load_image(data, encoding='base64', file_format='png'):
    """ Upload image """

    if data is None:
        return data

    url = '../data/load/'
    url_opt = url + 'opt/'

    if encoding == 'base64':
        file_format = re.search(r'data:image/.+;base64,', data).group()[11:-8]
        b64 = data.split(',')[1]
        data = base64.b64decode(b64)

    file_id = max_image(url)
    file_id = '{}{}{}'.format(
        '0' * max(0, 10-len(str(file_id))),
        file_id,
        ''.join(random.choice(string.ascii_lowercase) for _ in range(6)),
    )
    file_format = file_format.lower()
    file_name = '{}.{}'.format(file_id, file_format)
    url += file_name
    url_opt += file_name

    with open(url, 'wb') as file:
        file.write(data)

    # EXIF data
    # pylint: disable=W0212

    try:
        img = Image.open(url)
        orientation = None

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            img = img.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            img = img.transpose(Image.ROTATE_90)

        img.save(url)
        img.close()

    except (AttributeError, KeyError, IndexError):
        pass

    # Optimized version

    img = Image.open(url)

    if img.size[0] > img.size[1]:
        hpercent = (SIDE_OPTIMIZED / float(img.size[1]))
        wsize = int(float(img.size[0]) * float(hpercent))
        img = img.resize((wsize, SIDE_OPTIMIZED), Image.ANTIALIAS)
    else:
        wpercent = (SIDE_OPTIMIZED / float(img.size[0]))
        hsize = int(float(img.size[1]) * float(wpercent))
        img = img.resize((SIDE_OPTIMIZED, hsize), Image.ANTIALIAS)

    img.save(url_opt)

    # Response

    return file_name

def reimg(text):
    """ Load all images images from the text to the server """

    if text is None:
        return text

    # Base64
    while True:
        fragment = re.search(
            r'<img [^>]*src=[^>]+data:image/\w+;base64,[^\'">]+=[^>]+>', text
        )

        if fragment is None:
            break

        first, last = fragment.span()
        meta_fragment = re.search(
            r'data:image/\w+;base64,[^\'">]+=', fragment.group()
        )

        meta_first, meta_last = meta_fragment.span()
        data = load_image(meta_fragment.group())
        text = text[:first+meta_first] \
               + '/load/' + data \
               + text[first+meta_last:]

    # External links
    while True:
        fragment = re.search(
            r'<img [^>]*src=[^\'">]*[\'"][^\'">]*http[^\'">]+[^>]*>', text
        )

        if fragment is None:
            break

        first, last = fragment.span()
        meta_fragment = re.search(
            r'http[^\'">]+', fragment.group()
        )

        meta_first, meta_last = meta_fragment.span()
        link = meta_fragment.group()
        data = requests.get(link).content

        if '.' in link:
            file_format = link.split('.')[-1]

            if (
                'latex' in file_format
                or '/' in file_format
                or len(file_format) > 5
            ):
                file_format = 'png'

        else:
            file_format = None

        data = load_image(data, encoding='bytes', file_format=file_format)
        text = text[:first+meta_first] \
               + '/load/' + data \
               + text[first+meta_last:]

    return text
