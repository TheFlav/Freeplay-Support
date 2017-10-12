#!/bin/sh
pwd=$(pwd)
if [ "$pwd" -ne "/home/pi/Freeplay/Freeplay-Support/" ] ; then
  echo "This script should be run from /home/pi/Freeplay/Freeplay-Support/ !"
  exit
fi

cp GPIO\ Controller\ 1.cfg /opt/retropie/configs/all/retroarch-joypads
cp es_input.cfg /opt/retropie/configs/all/emulationstation/
sed -i -e '$i \python /home/pi/Freeplay/Freeplay-Support/shutdown_daemon.py &\n' rc.local
sudo cp autostart.sh /opt/retropie/configs/all
sudo cp freeplaycfg.txt /boot
sudo cp fpstartup.py /boot
