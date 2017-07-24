#!/usr/bin/python
# -*- coding: utf-8 -*-

# See https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=150358

#!/usr/bin/python

#
# Original Author:       Paul W. Versteeg
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    To get a copy of the GNU General Public License
#    go to <http://www.gnu.org/licenses/>
#-------------------------------------------------------------------------------
#

import RPi.GPIO as GPIO
from time import sleep, time, strftime
import subprocess
import sys
import socket
import os

# ==== constants
__author__ = 'original from Paul W. Versteeg, hacked by Ed'
VERSION = "3.1-"

# ==== GPIO setup
STOP_REQ = 20 # Stop/start button input, active low to shutdown RPi

def init():
      '''
      Initializes a number of settings and prepares the environment
      before we start the main application.

      '''
      global wd_ping, pwr_at_boot
      GPIO.setmode(GPIO.BCM)

      # This port is connected to a button
      # It is used to shutdown the RPi without the automatic restart
      GPIO.setup(STOP_REQ, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

      # setup the event to detect the button press to powerdown the RPi
      GPIO.add_event_detect(STOP_REQ, GPIO.RISING, callback=stop_req, bouncetime=20)

def stop_req(STOP_REQ):
      '''
      Interrupt service routine that gets called when the start/stop button
      is pressed while the RPi is running.

      Powerdown in this case means that the RPI will become powerless and the
      systemd watchdog will reboot the RPi in 10 seconds after poweroff.

      To avoid incorrect button presses, the button must be pressed for >1 seconds
      otherwise, it is deemed an invalid request.

      '''
      edge_start = time() # create a timestamp reference
      # print 'edge_start=',edge_start
      while (time() - edge_start) <= 2.0 : # check within a 2 Sec window
          if GPIO.input(STOP_REQ) == 0 : 
              # False signal
              # print 'false signal time() - edge_start=',(time() - edge_start)
              return

      # print 'time() - edge_start=',(time() - edge_start)
      # print 'time()',time()

      # remove the edge detection for the duration of this ISR
      GPIO.remove_event_detect(STOP_REQ)

      subprocess.call(['sudo poweroff'], shell=True, \
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():

      init()

      while True :
            # wait for a button press to shutdown the RPi
            # sleep to be nice
            sleep(60)


if __name__ == '__main__':
      main()

