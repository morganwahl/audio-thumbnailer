#!/usr/bin/env python

import sys
import os
import subprocess
import tempfile

from optparse import OptionParser

from PIL import Image

from mood_thumbnailer import fracticulate

MOODBAR_EXECUTABLE="moodbar"
#LOGFILE = open('/home/morgan/moodbar.log', 'wb')

#LOGFILE.write(repr(sys.argv) + "\n")

usage = 'usage: %prog [options] <audio file>'
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
    help="write the PNG thumbnail to FILE (defaults to stdout)",
)

(options, args) = parser.parse_args()

if len(args) < 1:
    exit("please give an audio file to thumbnail")

infile_name = args[0]

if (options.outfile is None):
    outfile = sys.stdout
else:
    outfile = open(options.outfile, 'wb')

mood_file = tempfile.NamedTemporaryFile(delete=False)
mood_file.close()
# generate the mood

# binary search for the longest power-of-4 length that will actually work
# the highest is simply size ^ 2
length_worked = False
length = options.size ** 2
while (not length_worked):
    #LOGFILE.write("trying length %d\n" % length)
    moodbar_args = (MOODBAR_EXECUTABLE, '-s', '512', '-l', unicode(length), '-o', mood_file.name, infile_name)
    moodbar_proc = subprocess.Popen(args=moodbar_args, stdout=tempfile.TemporaryFile())
    moodbar_proc.wait()

    actual_length = os.path.getsize(mood_file.name) / 3
    #LOGFILE.write("actual length was %d\n" % actual_length)
    if actual_length < length:
        length = length / 4
    else:
        length_worked = True

mood = open(mood_file.name)

# read the file 3 bytes at a time
inbytes = mood.read()
colors = []
for i in range( len(inbytes) / 3 ) :
    offset = i * 3
    rgb = []
    for j in range(3):
        rgb.append( ord(inbytes[offset + j]) )
    colors.append('|'.join(map(str, rgb)))

mood.close()
os.remove(mood_file.name)

# now turn the color tuples into an image
pixels = fracticulate(colors, ('tl', 'tr'))

if pixels is None:
    sys.exit(1)

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
