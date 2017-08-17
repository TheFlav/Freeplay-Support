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
VERSION = "3.2-Freeplay-02"

# ==== GPIO setup
STOP_REQ = 20 # Stop/start button input, active low to shutdown RPi
LOW_BATT = 7  # GPIO7 = low batt from MCU supervisor chip

pwr_btn_timeout = 4.0   # how many seconds does the power button need to be held
pwr_btn_edge_start = 0

low_batt_timeout = 60.0
low_batt_edge_start = 0



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
      GPIO.setup(LOW_BATT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

      # setup the event to detect the button press to powerdown the RPi
      GPIO.add_event_detect(STOP_REQ, GPIO.RISING, callback=stop_req, bouncetime=20)
      GPIO.add_event_detect(LOW_BATT, GPIO.FALLING, callback=low_batt_req, bouncetime=20)
      return

def pwr_btn_falling(STOP_REQ):
      global pwr_btn_edge_start
      # remove the edge detection for the duration of this ISR
      GPIO.remove_event_detect(STOP_REQ)
      pwr_btn_edge_start=0
      #print 'power button fell'
      GPIO.add_event_detect(STOP_REQ, GPIO.RISING, callback=stop_req, bouncetime=20)
      return

def low_batt_rising(LOW_BATT):
      global low_batt_edge_start
      # remove the edge detection for the duration of this ISR
      GPIO.remove_event_detect(LOW_BATT)
      low_batt_edge_start=0
      #print 'low batt detect rose'
      GPIO.add_event_detect(LOW_BATT, GPIO.FALLING, callback=low_batt_req, bouncetime=20)
      return

def stop_req(STOP_REQ):
      global pwr_btn_edge_start
      '''
      Interrupt service routine that gets called when the start/stop button
      is pressed while the RPi is running.

      Powerdown in this case means that the RPI will become powerless and the
      systemd watchdog will reboot the RPi in 10 seconds after poweroff.

      To avoid incorrect button presses, the button must be pressed for >1 seconds
      otherwise, it is deemed an invalid request.

      '''
      # remove the edge detection for the duration of this ISR
      GPIO.remove_event_detect(STOP_REQ)
      
      GPIO.add_event_detect(STOP_REQ, GPIO.FALLING, callback=pwr_btn_falling, bouncetime=20)
      pwr_btn_edge_start = time() # create a timestamp reference
      #print 'stop_req: pwr_btn_edge_start=',pwr_btn_edge_start
      return


def low_batt_req(LOW_BATT):
      global low_batt_edge_start
      '''
      Interrupt service routine that gets called when the low battery indicator
      goes low while the RPi is running.

      Powerdown in this case means that the RPI will become powerless and the
      systemd watchdog will reboot the RPi in 10 seconds after poweroff.

      To avoid incorrect button presses, the button must be pressed for >1 seconds
      otherwise, it is deemed an invalid request.

      '''
      # remove the edge detection for the duration of this ISR
      GPIO.remove_event_detect(LOW_BATT)
      
      GPIO.add_event_detect(LOW_BATT, GPIO.RISING, callback=low_batt_rising, bouncetime=20)
      low_batt_edge_start = time() # create a timestamp reference
      #print 'low_batt_req: low_batt_edge_start=',low_batt_edge_start
      return

def main():
      global pwr_btn_edge_start
      global low_batt_edge_start
      init()

      while True :
            # wait for a button press to shutdown the RPi
            # sleep to be nice
            if pwr_btn_edge_start <= 0 and low_batt_edge_start <= 0 :
                #print 'sleep ',pwr_btn_timeout
                sleep(pwr_btn_timeout) #sleep for the smallest timeout period
            else :
                #print 'sleep 0.1'
                sleep(0.1)
      
            temp_time = time()
            if pwr_btn_edge_start > 0 :
                #print 'main: pwr_btn_edge_start=',pwr_btn_edge_start
                #print 'main: temp_time=',temp_time,'  (temp_time - pwr_btn_edge_start)=',(temp_time - pwr_btn_edge_start)
                #print 'main: pwr_btn_timeout=',pwr_btn_timeout
                if ((temp_time - pwr_btn_edge_start)) > pwr_btn_timeout :
                    #print 'SHUTTING DOWN from PWR BTN'
                    #print ''
                    if GPIO.input(STOP_REQ) == 1 : 
                        GPIO.remove_event_detect(STOP_REQ)
                        GPIO.remove_event_detect(LOW_BATT)
                        subprocess.call(['sudo poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return
                    else :
                        GPIO.remove_event_detect(STOP_REQ)
                        pwr_btn_edge_start=0
                        #print '(FAILSAFE) power button fell'
                        GPIO.add_event_detect(STOP_REQ, GPIO.RISING, callback=stop_req, bouncetime=20)
  

            #print 'main: low_batt_edge_start=',low_batt_edge_start
            if low_batt_edge_start > 0 :
                if ((time() - low_batt_edge_start)) > low_batt_timeout :
                    #print 'SHUTTING DOWN from LOW BATT'
                    if GPIO.input(LOW_BATT) == 0 :
                        GPIO.remove_event_detect(STOP_REQ)
                        GPIO.remove_event_detect(LOW_BATT)
                        subprocess.call(['sudo poweroff'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        return
                    else :
                        GPIO.remove_event_detect(LOW_BATT)
                        low_batt_edge_start=0
                        #print '(FAILSAFE) low batt rose'
                        GPIO.add_event_detect(LOW_BATT, GPIO.FALLING, callback=low_batt_req, bouncetime=20)

if __name__ == '__main__':
      main()

