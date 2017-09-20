# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt
# edited by Ed for RPi

import os, struct, array, thread
from fcntl import ioctl
from subprocess import call

# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
print ""

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')
print ""

# Get the device name.
#buf = bytearray(63)
buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print '%d axes found: %s' % (num_axes, ', '.join(axis_map))
print '%d buttons found:\n%s' % (num_buttons, ', '.join(button_map))
print ""
print ""

def event_thread():
  # Main event loop
  while True:
    global jsdev
    global button_states
    global axis_states
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)

#        if type & 0x80:
#             print "(initial)",

        if type & 0x01:
            button = button_map[number]
            if button:
                button_states[button] = value
#                if value:
#                    print "%s pressed" % (button)
#                else:
#                    print "%s released" % (button)

        if type & 0x02:
            axis = axis_map[number]
            if axis:
                fvalue = value / 32767.0
                axis_states[axis] = fvalue
#                print "%s: %.3f" % (axis, fvalue)
  return



thread.start_new_thread(event_thread, ())


def btn_test(btn_name, num_times):
  test_num = 1
  while(test_num <= num_times) :
    if(btn_name == 'mode'):
      print 'Double tap PWR to press "mode"'
    if(num_times > 1) :
      print 'Press button "%s" (%d of %d)' % (btn_name, test_num, num_times)
    else :
      print 'Press button "%s"' % (btn_name)

    while (button_states[btn_name] == 0) :
      if((button_states['tr'] == 1) and (button_states['tl'] == 1)) :
        print '*** Skipping button "%s" test ***' % (btn_name)
        while(button_states['tr'] == 1 or button_states['tl'] == 1) :
          continue
        return
    while (button_states[btn_name] == 1) :
      continue
    test_num+=1
  return


def dpad_test(num_times):
  test_num = 1
  while(test_num <= num_times) :
    print 'Press dpad left (%d of %d)' % (test_num,num_times)
    while (axis_states['x'] >= 0) :
      continue
    while (axis_states['x'] < 0) :
      continue
    test_num+=1

  test_num = 1
  while(test_num <= num_times) :
    print 'Press dpad right (%d of %d)' % (test_num,num_times)
    while (axis_states['x'] <= 0) :
      continue
    while (axis_states['x'] > 0) :
      continue
    test_num+=1

  test_num = 1
  while(test_num <= num_times) :
    print 'Press dpad up (%d of %d)' % (test_num,num_times)
    while (axis_states['y'] >= 0) :
      continue
    while (axis_states['y'] < 0) :
      continue
    test_num+=1

  test_num = 1
  while(test_num <= num_times) :
    print 'Press dpad down (%d of %d)' % (test_num,num_times)
    while (axis_states['y'] <= 0) :
      continue
    while (axis_states['y'] > 0) :
      continue
    test_num+=1
  return

dpad_test(3)

print "BUTTON TESTS"
print "  Press both shoulder buttons"
print "       to skip a test."

btn_num = 0
while (btn_num < num_buttons) :
  btn_test(button_map[btn_num], 3)
  btn_num+=1

print ""
print "Speaker (Mono Right Only) Audio Test:"
print "  REMOVE HEADPHONES from jack"
print "    Set volume wheel to full volume"
print "    Actuate volume wheel during"
print "      Center and WahWah"
btn_test('a', 1)
call(["omxplayer", "/home/pi/Freeplay/Freeplay-Support/audiotest.mp4"])

print ""
print "Headphone Stereo Audio Test:"
print "  INSERT HEADPHONES into jack"
print "    Set volume wheel to full volume"
print "    Actuate volume wheel during"
print "      Center and WahWah"
btn_test('a', 1)
call(["omxplayer", "/home/pi/Freeplay/Freeplay-Support/audiotest.mp4"])


print ""
print "Test Complete"
btn_test('a', 1)