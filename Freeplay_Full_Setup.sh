#!/usr/bin/env bash

ADDONS=( TheFlav/FreeplaySupport mootikins/FreeplayILI9341 TheFlav/mk_arcade_joystickrpi TheFlav/rpi-fbcp TheFlav/setPCA9633 )
OPTIONS=$( printf '%s\n' "${ADDONS[@]}" | awk '{print $1, v++, "on" }')

cmd=(dialog --title "Install Addons" \
	--separate-output \
	--ok-label "Install" \
	--checklist "Select options:" 0 0 0)

CHOICES=$("${cmd[@]}" ${OPTIONS} 2>&1 >/dev/tty)

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
	printf "\nDownloading module ${ADDONS["$ADDON"]}...\u001b[0m\n"
	if git clone https://github.com/${ADDONS["$ADDON"]} ; then
		printf "\u001b[32mModule ${ADDONS["$ADDON"]} downloaded successfully\u001b[0m\n"
	else
		printf "\e[0;31;40mModule ${ADDONS["$ADDON"]} was NOT downloaded successfully\u001b[0m\n"
		DL_ERR+=( "$ADDON" )
	fi
done

INST_ERR=()

for DIR in $(ls -d */)
do
	pushd $DIR &> /dev/null
	printf "\u001b[36;1mInstalling $DIR...\u001b[0m\n"
####################
# TODO Add Install #
####################
	popd &> /dev/null
done
popd &> /dev/null

printf "The following modules could not be downloaded:\n"
for MODULE in ${DL_ERR[@]}
do
	printf "\t\e[0;31;40m${ADDONS["$MODULE"]}\u001b[0m\n"
done


