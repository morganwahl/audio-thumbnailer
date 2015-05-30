#!/usr/bin/env python

# a mood is a bunch of RGB triples

import sys

from optparse import OptionParser

import Image

from audio_thumbnailer.fracticulate import fracticulate

def main():
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

    infile = open(args[0], 'rb')

    if options.outfile is None:
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'wb')

    # read the file 3 bytes at a time
    inbytes = infile.read()
    colors = []
    for i in range(len(inbytes) / 3):
        offset = i * 3
        rgb = []
        for j in range(3):
            rgb.append(ord(inbytes[offset + j]))
        colors.append('|'.join(map(str, rgb)))

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

    im.save(outfile, 'png')

if __name__ == '__main__':
    main()
