#!/bin/sh

if [ "$PWD" != "/home/pi/Freeplay/Freeplay-Support" ] ; then
  echo "This script should be run from /home/pi/Freeplay/Freeplay-Support/ !"
  exit
fi

cp GPIO\ Controller\ 1.cfg /opt/retropie/configs/all/retroarch-joypads
cp es_input.cfg /opt/retropie/configs/all/emulationstation/

if grep -q "python /home/pi/Freeplay/Freeplay-Support/shutdown_daemon.py &" /etc/rc.local; then
    echo "/etc/rc.local already contains shutdown script"
else
    sudo sed -i -e '$i \python /home/pi/Freeplay/Freeplay-Support/shutdown_daemon.py &\n' /etc/rc.local
fi
sudo cp autostart.sh /opt/retropie/configs/all
sudo cp freeplaycfg.txt /boot
sudo cp fpstartup.py /boot
