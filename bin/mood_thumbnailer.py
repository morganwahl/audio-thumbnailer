#!/usr/bin/env python

import logging
import os
import sys

if __name__ == '__main__':
    _HERE = os.path.dirname(os.path.abspath(__file__))
    if _HERE in sys.path:
        sys.path.remove()
    del _HERE

    _LIB = os.path.join(
        os.environ['HOME'],
        'audio-thumbnailer',
    )
    sys.path.insert(0, _LIB)
    del _LIB


from optparse import OptionParser

import Image

from audio_thumbnailer.fracticulate import fracticulate
from audio_thumbnailer.moodbar import read_mood_file

def main():
    logging.basicConfig(level='DEBUG')

    usage = 'usage: %prog [options] <mood file>'
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-s",
        "--size",
        type='int',
        default=256,
        metavar='SIZE',
        help="output a image of SIZE x SIZE (defaults to %default)",
    )
    parser.add_option(
        "-o",
        "--output-file",
        dest="outfile",
        metavar='FILE',
        help="write the thumbnail to FILE (defaults to stdout)",
    )

    (options, args) = parser.parse_args()

    if len(args) < 1:
        exit("please give a .mood file to render")

    colors = read_mood_file(args[0])

    # now turn the color tuples into an image
    pixels = fracticulate(colors, ('tl', 'tr'))

    im = Image.new('RGB', pixels.shape)

    raveled = []
    for p in pixels.ravel():
        if p is None:
            raveled.append((0, 0, 0))
        else:
            raveled.append(tuple(map(int, p.split('|'))))
    im.putdata(raveled)
    im = im.resize((options.size,) * 2, Image.NEAREST)

    if options.outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'wb')

    im.save(outfile, 'png')

if __name__ == '__main__':
    main()
