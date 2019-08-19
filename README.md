# Freeplay-Support

### One Line Installer
To install any of these modules on a fresh RetroPie image, use the following one-liner:
```
bash -c "$(wget -O- https://raw.githubusercontent.com/TheFlav/Freeplay-Support/master/Full_Install.sh)"
```
It will use a checklist to let you select what modules you would like to install, then download and install them.

If you are starting from a fresh Raspbian image, make sure to enable ssh first and add the following lines to `/boot/config.txt` (More info can be found [HERE](https://docs.google.com/document/d/1jsMiFlVP3VeDBXceNmpgAKqP-99v2K9L3xj09K-zHSQ/edit#)):
```
# BEGIN FREEPLAY MODS
framebuffer_width=320
framebuffer_height=240
hdmi_force_hotplug=1   #these HDMI lines will try to set up 1024x768 (you can remove them if you have problems playing via HDMI)
HDMI_FORCE_MODE=1
hdmi_group=2
hdmi_mode=16
hdmi_drive=1           #Normal DVI mode (No sound) (2 for HDMI with sound)
dtparam=spi=on
dtparam=audio=on
[pi0]
#Freeplay Zero
dtoverlay=audremap,swap_lr=off
dtoverlay=waveshare32b,speed=80000000,fps=60,rotate=270
[pi3]
#Freeplay CM3
dtoverlay=audremap,swap_lr=on
dtoverlay=waveshare32b,speed=99999999,fps=60,rotate=270
dtparam=i2c1_baudrate=400000 #makes a big speed difference
dtoverlay=i2c1-bcm2708,sda1_pin=44,scl1_pin=45,pin_func=6
[pi2]
#Sometimes we test with Pi2
dtoverlay=audremap,swap_lr=on
dtoverlay=waveshare32b,speed=80000000,fps=60,rotate=270
[all]
dtoverlay=gpio-poweroff,gpiopin=21,active_low
# Disable the ACT LED on the Pi Zero.
dtparam=act_led_trigger=none
dtparam=act_led_activelow=on
audio_pwm_mode=2
dtparam=watchdog=on # Enabling watchdog.
# remove # from following 2 lines to turn wifi and bluetooth off (if not needed, can Speed Up Pi Zero W)
#dtoverlay=pi3-disable-wifi
#dtoverlay=pi3-disable-bt
# END FREEPLAY MODS
```

#### Ports
Information about ports (other games you can add) can be found [HERE](./Ports.md)
