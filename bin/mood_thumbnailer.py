#!/usr/bin/env python

# a mood is a bunch of RGB triples

import sys
from math import log, ceil

from optparse import OptionParser

from numpy import array, vstack, hstack

import Image

def fracticulate(seq, from_to):
    '''\
    given a sequence, returns a 2-d array using a fractal arrangement
    that ensures elements that are close to each other in the sequence are
    close in the 2-d array. the sequence will be padded with Nones until
    it's length is a power of 4.
    '''

    if len(seq) < 1:
        return None

    if len(seq) == 1:
        return array(seq)

    log_4 = log(len(seq), 4)

    if log_4 != int(log_4):
        # pad the sequence to be a power-of-four

        # find lowest power of four >= the sequence length
        # this could potentially be re-written make use of bit-maniputian tricks instead of floating-point arithmatic
        # TODO does int() round or just truncate?
        power = int(ceil(log_4))

        seq = list(seq) + [None,] * (4 ** power - len(seq))

    step = len(seq) / 4

    if from_to == ('tl', 'tr'):
        tl = fracticulate(seq[step * 0: step * 1], ('tl', 'bl'))
        bl = fracticulate(seq[step * 1: step * 2], ('tl', 'tr'))
        br = fracticulate(seq[step * 2: step * 3], ('tl', 'tr'))
        tr = fracticulate(seq[step * 3: step * 4], ('br', 'tr'))
    if from_to == ('tl', 'bl'):
        tl = fracticulate(seq[step * 0: step * 1], ('tl', 'tr'))
        tr = fracticulate(seq[step * 1: step * 2], ('tl', 'bl'))
        br = fracticulate(seq[step * 2: step * 3], ('tl', 'bl'))
        bl = fracticulate(seq[step * 3: step * 4], ('br', 'bl'))
    if from_to == ('br', 'tr'):
        br = fracticulate(seq[step * 0: step * 1], ('br', 'bl'))
        bl = fracticulate(seq[step * 1: step * 2], ('br', 'tr'))
        tl = fracticulate(seq[step * 2: step * 3], ('br', 'tr'))
        tr = fracticulate(seq[step * 3: step * 4], ('tl', 'tr'))
    if from_to == ('br', 'bl'):
        br = fracticulate(seq[step * 0: step * 1], ('br', 'tr'))
        tr = fracticulate(seq[step * 1: step * 2], ('br', 'bl'))
        tl = fracticulate(seq[step * 2: step * 3], ('br', 'bl'))
        bl = fracticulate(seq[step * 3: step * 4], ('tl', 'bl'))

    l = vstack((tl, bl))
    r = vstack((tr, br))

    return hstack((l, r))

if __name__ == '__main__':
    usage = 'usage: %prog [options] <mood file>'
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--size",
        type='int',
        default=256,
        metavar='SIZE',
        help="output a image of SIZE x SIZE (defaults to %default)",
    )
    parser.add_option("-o", "--output-file",
        dest="outfile",
        metavar='FILE',
        help="write the thumbnail to FILE (defaults to stdout)",
    )

    (options, args) = parser.parse_args()

    if len(args) < 1:
        exit("please give a .mood file to render")

    infile = open(args[0], 'rb')

    if (options.outfile is None):
        outfile = sys.stdout
    else:
        outfile = open(options.outfile, 'wb')

    # read the file 3 bytes at a time
    inbytes = infile.read()
    colors = []
    for i in range( len(inbytes) / 3 ) :
        offset = i * 3
        rgb = []
        for j in range(3):
            rgb.append( ord(inbytes[offset + j]) )
        colors.append('|'.join(map(str, rgb)))

    # now turn the color tuples into an image
    pixels = fracticulate(colors, ('tl', 'tr'))

    im = Image.new('RGB', pixels.shape)

    raveled = []
    for p in pixels.ravel():
        if p is None:
            raveled.append( (0,0,0) )
        else:
            raveled.append(tuple(map(int, p.split('|'))))
    im.putdata(raveled)
    im = im.resize((options.size,) * 2, Image.NEAREST)

    im.save(outfile, 'png')

