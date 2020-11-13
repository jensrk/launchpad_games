import time
import rtmidi

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

def update_all(val):
	with midi_out:
		for i in range(8):
			midi_out.send_message([0xB0, 104+i, val])
		for i in range(8):
			for j in range(9):
				midi_out.send_message([0x90, i*16+j, val])

update_all(127)

del midi_out
del midi_in