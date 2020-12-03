import time
import rtmidi
import numpy as np
from game_of_life import GameOfLife

RED_HI = 3
GREEN_HI = 48
ORANGE_HI = 50
DELAY = 0.001

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

global grid
grid = np.zeros([8,8])

def init():
    midi_out.send_message([144, 120, RED_HI])

def update_all(val):
    for i in range(8):
        midi_out.send_message([0xB0, 104+i, val])
        time.sleep(DELAY)
    for i in range(8):
        for j in range(9):
            midi_out.send_message([0x90, i*16+j, val])
            time.sleep(DELAY)

mapping = np.zeros([8,8], dtype=np.int32)
for i in range(8):
    for j in range(8):
        mapping[i,j] = i*16 + j

def update_grid(new):
    global grid
    for val in mapping[(grid != new) * new]:
        out = [144, val, ORANGE_HI]
        midi_out.send_message(out)
        time.sleep(DELAY)
    for val in mapping[(grid != new) * (1 - new) == 1]:
        out = [144, val, 0]
        midi_out.send_message(out)
        time.sleep(DELAY)
    grid = new.copy()

init()
life = GameOfLife([8,8])
speed = 0

last_cycle = time.time()
try:
    while True:
        msg = midi_in.get_message()
        if msg:
            if msg[0][2] != 0:
                if msg[0][0] == 144:
                    if msg[0][1] % 16 == 8:
                        speed = 7 - int(msg[0][1] / 16)
                        print("Set speed to", speed)
                        for i in range(7):
                            out = [144, 16*i+8, GREEN_HI if (7-i) <= speed else 0]
                            midi_out.send_message(out)
                            time.sleep(DELAY)
                        if speed == 0:
                            life.step()
                            update_grid(life.board)
                    elif msg[0][2] == 127:
                        x = msg[0][1] % 16
                        y = int(msg[0][1] / 16)
                        life.toggle_cell(x,y)
                        update_grid(life.board)
        if speed > 0:
            now = time.time()
            if now >= last_cycle + 1 / speed:
                life.step()
                update_grid(life.board)
                last_cycle = now
        time.sleep(DELAY)

except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midi_in.close_port()
    update_all(0)
    midi_out.close_port()
    del midi_in
    del midi_out