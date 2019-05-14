#!/bin/sh
 sudo apt install watchdog

 if sudo grep -q -e "^watchdog-timeout" /etc/watchdog.conf ; then
	 printf "Watchdog timeout already defined\nRecommended value is 15\n"
 else
	sudo echo "watchdog-timeout = 15" >> /etc/watchdog.conf
fi

 sudo systemctl enable watchdog.service

 if sudo grep -q "Starting software Watchdog" /etc/rc.local ; then
	 echo "Software watchdog already installed"
 else
	 sudo sed -i 's|^exit 0|printf "Starting software Watchdog"\n/usr/sbin/service watchdog start &\n\nexit 0|' /etc/rc.local
 fi
