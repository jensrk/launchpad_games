import time
import rtmidi

OFF = 0
RED_LO = 1
RED_MI = 2
RED_HI = 3

GREEN_LO = 16
GREEN_MI = 32
GREEN_HI = 48

YELLOW_LO = 17
YELLOW_MI = 33
YELLOW_HI = 49

ORANGE_LO = 18
ORANGE_MI = 34
ORANGE_HI = 50

RORANGE_LO = 19
RORANGE_MI = 35
RORANGE_HI = 51

color_bar = {0: 0, 1: 16, 2: 32, 3: 48, 4: 49, 5: 50, 6: 33, 7: 51, 8: 34, 9: 17, 10: 18, 11: 35, 12: 19, 13: RED_HI, 14: RED_MI, 15: RED_LO}

global selected_color
selected_color = 0

midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()
in_ports = midi_in.get_ports()
launchpad_in = [i for (i,s) in enumerate(in_ports) if s.find('Launchpad') >= 0]
out_ports = midi_out.get_ports()
launchpad_out = [i for (i,s) in enumerate(out_ports) if s.find('Launchpad') >= 0]


if launchpad_in and launchpad_out:
	midi_in.open_port(launchpad_in[0])
	midi_out.open_port(launchpad_out[0])
else:
	print('Launchpad not found.')
	exit()
	
def init_sketchpad():
	for i in range(8):
		midi_out.send_message([0xB0, 104+i, color_bar[i]])
		midi_out.send_message([0x90, 8+16*i, color_bar[i+8]])
			

def update_all(val):
	for i in range(8):
		midi_out.send_message([0xB0, 104+i, val])
	for i in range(8):
		for j in range(9):
			midi_out.send_message([0x90, i*16+j, val])

#update_all(127)

print("Entering main loop. Press Control-C to exit.")
update_all(0)
init_sketchpad()
try:
	timer = time.time()
	while True:
		msg = midi_in.get_message()
		if msg:
			print(msg)
			if msg[0][0] == 176:
				selected_color = msg[0][1] - 104
			elif msg[0][0] == 144:
				if msg[0][1] % 16 == 8:
					selected_color = int(msg[0][1] / 16) + 8
				else:
					out = [144, msg[0][1], color_bar[selected_color]]
					print(out)
					midi_out.send_message(out)
		time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
	print("Exit.")
	update_all(0)
	midi_in.close_port()
	midi_out.close_port()
	del midi_in
	del midi_out

#			if message[0] == 144:
#				with midi_out:
#					midi_out.send_message([144, message[1], RORANGE_HI]])