import os
import subprocess
import tempfile

MOODBAR_EXECUTABLE = "moodbar"


def audio_get_colors(infile_name, size):
    mood_file = tempfile.NamedTemporaryFile(delete=False)
    mood_file.close()
    # generate the mood

    # binary search for the longest power-of-4 length that will actually work
    # the highest is simply size ^ 2
    length_worked = False
    length = size ** 2
    while not length_worked:
        #LOGFILE.write("trying length %d\n" % length)
        moodbar_args = (
            MOODBAR_EXECUTABLE,
            '-s', '512',
            '-l', unicode(length),
            '-o', mood_file.name,
            infile_name
        )
        moodbar_proc = subprocess.Popen(
            args=moodbar_args, stdout=tempfile.TemporaryFile()
        )
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
    for i in range(len(inbytes) / 3):
        offset = i * 3
        rgb = []
        for j in range(3):
            rgb.append(ord(inbytes[offset + j]))
        colors.append('|'.join(map(str, rgb)))

    mood.close()
    os.remove(mood_file.name)

    return colors
