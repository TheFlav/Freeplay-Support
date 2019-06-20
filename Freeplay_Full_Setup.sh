#!/usr/bin/env bash

ADDONS=( TheFlav/Freeplay-Support mootikins/FreeplayILI9341 TheFlav/mkarcade_joystick_rpi TheFlav/rpi-fbcp TheFlav/setPCA9633 )
OPTIONS=$( printf '%s\n' "${ADDONS[@]}" | awk '{print v++, $1, "on" }')

cmd=(dialog --title "Install Addons" \
	--separate-output \
	--ok-label "Install" \
	--checklist "Select options:" 0 0 0)

CHOICES=$("${cmd[@]}" ${OPTIONS} 2>&1 >/dev/tty)

clear

####################
#   ToDo Remove    #
####################
rm -rf Freeplay

mkdir Freeplay

printf "Downloading selected Addons. If there are any prompts, press Enter."

pushd /home/pi/Freeplay/Freeplay-Support/Freeplay/ &> /dev/null

for ADDON in $CHOICES
do
	printf "\nDownloading module ${ADDONS["$ADDON"]}...\u001b[0m\n"
	if git clone https://github.com/${ADDONS["$ADDON"]} ; then
		printf "\u001b[32mModule ${ADDONS["$ADDON"]} downloaded successfully\u001b[0m\n"
	else
		printf "\e[5;31;40mModule ${ADDONS["$ADDON"]} was NOT downloaded successfully\u001b[0m\n"
	fi
done

for DIR in $(ls -d */)
do
	pushd $DIR &> /dev/null
####################
# ToDo Add Install #
####################
	popd &> /dev/null
done

popd &> /dev/null
