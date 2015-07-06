#!/bin/bash
#
# description: alfr3d init script
#
### BEGIN INIT INFO
# Provides:          alfr3d
# Required-Start:    $local_fs $network $mongod
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: alfr3d daemon
# Description:       alfr3d daemon
# Start the service alfr3d
### END INIT INFO

INITSAY="all alfred services have been initialized"
ENDSAY="Stopping all alfred services"
HOMEDIR=/home/armageddion/Alfr3d

start() {
    echo "Starting alfr3d services: " >> $HOMEDIR/log/init.log
    ### Create the lock file ###
    touch /var/lock/alfr3d

    ### Mount Samba share ###
    echo "Mounting aduio shares" >> $HOMEDIR/log/init.log
    sudo mount -t cifs -o user=alfr3d,password=alfr3d //10.0.0.3/Audio $HOMEDIR/../audio/ > $HOMEDIR/log/init.log &

    ### Start the daemon ###
    echo "Starting alfr3d daemon" >> $HOMEDIR/log/init.log
    python $HOMEDIR/daemon/alfr3ddaemon.py start >> $HOMEDIR/log/init.log &

    ### Start Node.js server ###
    echo "Starting node server" >> $HOMEDIR/log/init.log
    node $HOMEDIR/alfr3d.js/alfr3dServer.js > $HOMEDIR/log/init.log &

    ### Initialize resftul interface ###
    echo "Initializing restful interface" >> $HOMEDIR/log/init.log
    python $HOMEDIR/run/alfr3dBottle.py >> $HOMEDIR/log/init.log &

    ### Initialize Mongo Express admin UI ###
    echo "Initializing mongo admin UI" >> $HOMEDIR/log/init.log
    nodejs $HOMEDIR/../node_modules/mongo-express/app >> $HOMEDIR/log/init.log &

    sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$INITSAY"
}
# Restart the service alfr3d
stop() {
    echo "Stopping alfr3d services: "
    sudo mplayer -ao alsa:device=default -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$ENDSAY"
    python $HOMEDIR/daemon/alfr3ddaemon.py stop >> $HOMEDIR/log/init.log &
    killproc -TERM $HOMEDIR/run/alfr3dBottle.py
    killproc -TERM $HOMEDIR/alfr3d.js/alfr3dServer.js
    umount $HOMEDIR/../audio
    ### Now, delete the lock file ###
    rm -f /var/lock/alfr3d
    echo
}
### main logic ###
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status alfr3d
        ;;
  restart|reload|condrestart)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0

