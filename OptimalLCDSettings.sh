#!/usr/bin/env bash

dialog --title "Freeplay Optimal LCD Settings" \
	--yesno "Our 'optimal' settings are made for those that do not expect to use external displays via HDMI and would prefer sharper pixels when using an uncropped display driver. If you want reliable HDMI output without changing this setting or are using a normal GBA viewing window, do not use the optimal settings. Would you like to use them?" 15 60

RESP=$?
case $RESP in
	0) dialog --title "Using Optimal Settings" --infobox "640x480 resolution will be applied on next startup." 10 60;
		sudo sed -i 's/^hdmi_mode=16/hdmi_mode=4/' /boot/config.txt;;
	1) dialog --title "NOT Using Optimal Settings" --infobox "1024x768 resolution will be applied on next startup." 10 60;
		sudo sed -i 's/^hdmi_mode=4/hdmi_mode=16/' /boot/config.txt;;
	255) ;;
esac
