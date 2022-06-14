#!/usr/bin/env bash

# Modules can be added here in the following format:
# Tail_of_GitHub_URL Short_Description Default_Checkbox_State
# The description must use underscores instead of spaces
ADDONS=( \
"TheFlav/Freeplay-Support General_Freeplay_Tools on" \
"TheFlav/rpi-fbcp Original_display_driver_(Zero) on" \
"mootikins/FreeplayILI9341 Precompiled_advanced_display_driver_(Non-Zero) on" \
"TheFlav/mk_arcade_joystick_rpi GPIO_joystick_driver_with_related_tools on" \
"TheFlav/setPCA9633 PWM_Brightness_controller_(requires_add-on) on" \
"TheFlav/FreeplayAudioTools Audio_tools_for_HDMI_and_mono/stereo on" \
"Mootikins/Freeplay-Wireless-Menu Menu_for_toggling_Bluetooth/WiFi_on_Pi_Zero_ONLY off" \
)

cmd=(dialog --title "Install Addons" \
	--separate-output \
	--ok-label "Install" \
	--checklist "Select options:" 0 0 0)

CHOICES=$("${cmd[@]}" ${ADDONS[@]} 2>&1 >/dev/tty)
clear

mkdir /home/pi/Freeplay

printf "Downloading selected Addons. If there are any prompts, press Enter."

pushd /home/pi/Freeplay &> /dev/null

DL_ERR=()
for ADDON in $CHOICES
do
	printf "\nDownloading module "$ADDON"...\u001b[0m\n"
	if git clone https://github.com/"$ADDON" ; then
		printf "\u001b[32mModule "$ADDON" downloaded successfully\u001b[0m\n"
	else
		printf "\e[0;31;40mModule "$ADDON" was NOT downloaded successfully\u001b[0m\n"
		DL_ERR+=( "$ADDON" )
	fi
done

if [ ${#DL_ERR[@]} -eq 0 ]; then
	printf "\n\u001b[32mAll selected modules downloaded successfully\u001b[0m\n"
else
	printf "\n\e[0;31;40mThe following modules could not be downloaded:\u001b[0m\n"
	for MODULE in ${DL_ERR[@]}
	do
		printf "\t\e[0;31;40m"$MODULE"\u001b[0m\n"
	done
fi
sleep 1

INST_ERR=()
printf "\n\u001b[36;1mInstalling downloaded modules\u001b[0m\n"
for DIR in $(ls -d */)
do
	pushd $DIR &> /dev/null
	printf "\t\u001b[36;1m$DIR...\u001b[0m\n"

	if sudo ./install.sh; then
		printf "\u001b[36;1m$DIR Installed Successfully\u001b[0m\n"
	else
		printf "\e[0;31;40m$DIR NOT Installed Successfully\u001b[0m\n"
		INST_ERR+=( "$DIR" )
	fi

	popd &> /dev/null
done
popd &> /dev/null

if [ ${#INST_ERR[@]} -eq 0 ]; then
	printf "\n\u001b[32mAll downloaded modules installed successfully\u001b[0m\n"
else
	printf "\n\e[0;31;40mThe following modules could not be installed:\u001b[0m\n"
	for MODULE in ${INST_ERR[@]}
	do
		printf "\t\e[0;31;40m"$MODULE"\u001b[0m\n"
	done
fi

dialog --title "RxBrad Freeplay Theme" \
	--yesno "Would you like to download and install RxBrad's Freeplay theme for EmulationStation?" 0 0

RESP=$?
case $RESP in
	0) sudo git clone --recursive --depth 1 "https://github.com/rxbrad/es-theme-freeplay.git" "/etc/emulationstation/themes/freeplay"; \
		sudo sed -i 's/<string name="ThemeSet" value=".*" \/>/<string name="ThemeSet" value="freeplay" \/>/g' /opt/retropie/configs/all/emulationstation/es_settings.cfg; \
		sudo sed -i 's/<string name="TransitionStyle" value=".*" \/>/<string name="TransitionStyle" value="instant" \/>/' /opt/retropie/configs/all/emulationstation/es_settings.cfg;;
	1) ;;
	255) ;;
esac

mkdir -p "/home/pi/RetroPie/retropiemenu/Freeplay Options"
sudo cp /home/pi/Freeplay/Freeplay-Support/OptimalLCDSettings.sh "/home/pi/RetroPie/retropiemenu/Freeplay Options/OptimalLCDSettings.sh"

if grep -q "Freeplay Optimal LCD Settings" /opt/retropie/configs/all/emulationstation/gamelists/retropie/gamelist.xml ; then
	echo "Optimal LCD Settings Changer already in menu"
else
	sudo sed -i 's|</gameList>|\t<game>\n\t\t<path>./Freeplay Options/OptimalLCDSettings.sh</path>\n\t\t<name>Freeplay Optimal LCD Settings</name>\n\t\t<desc>Switch between optimal LCD settings and HDMI compatibility</desc>\n\t\t<image></image>\n\t\t<playcount>0</playcount>\n\t\t<lastplayed>20180514T205700</lastplayed>\n\t</game>\n</gameList>|' /opt/retropie/configs/all/emulationstation/gamelists/retropie/gamelist.xml
fi

exit 0
