import logging
import os
import subprocess
import tempfile

L = logging.getLogger(__name__)

MOODBAR_EXECUTABLE = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # audio_thumbnailer
    '..',  # repo
    'vendor',
    'moodbar-gst',
    'analyzer',
    'moodbar',
))

def read_mood_file(filename):
    # a mood file is a bunch of RGB triples

    with open(filename, 'rb') as infile:
        # just read the whole file
        inbytes = infile.read()

    # go through the data 3 bytes at a time
    colors = []
    for i in range(len(inbytes) / 3):
        offset = i * 3
        rgb = []
        for j in range(3):
            rgb.append(ord(inbytes[offset + j]))
        colors.append('|'.join(map(str, rgb)))

    return colors

def make_mood_file(audio_filename, mood_filename, size):
    # binary search for the longest power-of-4 length that will actually work
    # the highest is simply size ^ 2
    length_worked = False
    length = size ** 2
    while not length_worked:
        L.debug("trying length %d", length)
        moodbar_args = (
            MOODBAR_EXECUTABLE,
            '-s', '512',
            '-l', unicode(length),
            '-o', mood_filename,
            audio_filename
        )
        L.debug("Running %r", moodbar_args)
        moodbar_proc = subprocess.Popen(
            args=moodbar_args, stdout=tempfile.TemporaryFile()
        )
        moodbar_proc.wait()

        actual_length = os.path.getsize(mood_filename) / 3
        L.debug("actual length was %d", actual_length)
        if actual_length < length:
            length = length / 4
        else:
            length_worked = True

def audio_get_colors(infile_name, size):
    mood_file = tempfile.NamedTemporaryFile(delete=False)
    mood_file.close()
    # generate the mood

    make_mood_file(infile_name, mood_file.name, size)

    colors = read_mood_file(mood_file.name)

    os.remove(mood_file.name)

    return colors
