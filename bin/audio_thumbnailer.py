#!/usr/bin/env python

from __future__ import absolute_import

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

from PIL import Image

from audio_thumbnailer.fracticulate import fracticulate
from audio_thumbnailer.moodbar import audio_get_colors

L = logging.getLogger(__name__)

def main():
    logging.basicConfig(level='WARN')

    L.debug('%r', sys.argv)

    usage = 'usage: %prog [options] <audio file>'
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
        help="write the PNG thumbnail to FILE (defaults to stdout)",
    )

    (options, args) = parser.parse_args()

    if len(args) < 1:
        exit("please give an audio file to thumbnail")

    if options.outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'wb')

    colors = audio_get_colors(infile_name=args[0], size=options.size)

    # now turn the color tuples into an image
    pixels = fracticulate(colors, ('tl', 'tr'))

    if pixels is None:
        sys.exit(1)

    im = Image.new('RGB', pixels.shape)

    raveled = []
    for p in pixels.ravel():
        if p is None:
            raveled.append((0, 0, 0))
        else:
            raveled.append(tuple(map(int, p.split('|'))))
    im.putdata(raveled)
    im = im.resize((options.size,) * 2, Image.NEAREST)

    im.save(outfile, 'png')

if __name__ == '__main__':
    main()
