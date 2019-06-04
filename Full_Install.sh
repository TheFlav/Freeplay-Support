#!/usr/bin/env bash

# Modules can be added here in the following format:
# Tail_of_GitHub_URL Short_Description Default_Checkbox_State
# The description must use underscores instead of spaces
ADDONS=(
"TheFlav/Freeplay-Support General_Freeplay_Tools on"
"TheFlav/rpi-fbcp Original_display_driver_(Zero) on"
"mootikins/FreeplayILI9341 Precompiled_advanced_display_driver_(Non-Zero) on"
"TheFlav/mk_arcade_joystick_rpi GPIO_joystick_driver_with_related_tools on"
"TheFlav/setPCA9633 PWM_Brightness_controller_(requires_add-on) on"
)

cmd=(dialog --title "Install Addons" \
	--separate-output \
	--ok-label "Install" \
	--checklist "Select options:" 0 0 0)

CHOICES=$("${cmd[@]}" ${ADDONS[@]} 2>&1 >/dev/tty)
clear

####################
#   TODO Remove    #
####################
rm -rf Freeplay

mkdir Freeplay

printf "Downloading selected Addons. If there are any prompts, press Enter."

pushd /home/pi/Freeplay/Freeplay-Support/Freeplay/ &> /dev/null

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
	printf "\t\u001b[36;1m$DIR...\u001b[0m"

	if [ ./install.sh -eq 0 ]; then
		printf "\u001b[36;1mInstalled Successfully\u001b[0m"
	else
		printf "\e[0;31;40mInstalled Successfully\u001b[0m"
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
