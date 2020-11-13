import rtmidi

midiin = rtmidi.MidiIn()
midiout = rtmidi.MidiOut()
in_ports = midiin.get_ports()
out_ports = midiout.get_ports()

print('In ports: ', in_ports)
print('Out ports: ', out_ports)