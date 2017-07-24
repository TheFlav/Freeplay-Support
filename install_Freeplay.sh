#!/bin/sh

	echo "Installing required dependencies"
	sudo apt-get install -y --force-yes dkms cpp-4.7 gcc-4.7 joystick || 
         { echo "ERROR : Unable to install required dependencies" && exit 1 ;}
	echo "Downloading current kernel headers"
	wget http://www.niksula.hut.fi/~mhiienka/Rpi/linux-headers-rpi/linux-headers-`uname -r`_`uname -r`-2_armhf.deb || 
         { echo "ERROR : Unable to find kernel headers" && exit 1 ;}
	echo "Installing current kernel headers"
	sudo dpkg -i linux-headers-`uname -r`_`uname -r`-2_armhf.deb || 
         { echo "ERROR : Unable to install kernel headers" && exit 1 ;}
	rm linux-headers-`uname -r`_`uname -r`-2_armhf.deb

	echo "Do more stuff"