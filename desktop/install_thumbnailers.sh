#!/bin/bash

for mime in "application@x-mood"
do
  gconftool-2 -s -t string "/desktop/gnome/thumbnailers/${mime}/command" "$HOME/bin/mood_thumbnailer.py -s %s -o %o %i"
  gconftool-2 -s -t boolean "/desktop/gnome/thumbnailers/${mime}/enable" True
done

for mime in {"audio@flac","audio@x-wav","audio@mp4","audio@mpeg","audio@x-vorbis@ogg"}
do
  gconftool-2 -s -t string "/desktop/gnome/thumbnailers/${mime}/command" "$HOME/bin/audio_thumbnailer.py -s %s -o %o %i"
  gconftool-2 -s -t boolean "/desktop/gnome/thumbnailers/${mime}/enable" True
done

