#!/bin/bash
mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$*" 
#sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en-uk&q=$*"

# DEBUG STREAM for mplayer
#sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://mp3channels.webradio.antenne.de/chillout"
