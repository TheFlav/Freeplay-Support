#!/usr/bin/env bash

dialog --title "Freeplay Optimal LCD Settings" \
	--yesno "Would you like to use the optimal LCD settings? This may break HDMI comaptibility on most monitors/TVs" 0 0

RESP=$?
case $RESP in
	0) sudo sed -i 's/^hdmi_mode=16/hdmi_mode=4/' /boot/config.txt;;
	1) sudo sed -i 's/^hdmi_mode=4/hdmi_mode=16/' /boot/config.txt;;
	255) ;;
esac
