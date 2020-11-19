import time
import random
import rtmidi

GREEN_LO = 16
GREEN_HI = 48
BRIGHT_ORANGE = 51
RED_MI = 2
RED_HI = 3
UP = 104
DOWN = 105
LEFT = 106
RIGHT = 107

color_bar = {0: 0, 1: 16, 2: 32, 3: 48, 4: 49, 5: 50, 6: 33, 7: 51, 8: 34, 9: 17, 10: 18, 11: 35, 12: 19, 13: 3, 14: 2, 15: 1}

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

snake = [21, 22]
snake_length = 2
direction = LEFT
cycle_duration = .75
goodie_in = 5
goodie = -1
game_over = False
	
def init_sketchpad():
	for i in range(4):
		midi_out.send_message([0xB0, 104+i, GREEN_LO])
	midi_out.send_message([0xB0, direction, GREEN_HI])
	for field in snake:
		midi_out.send_message([144, field, BRIGHT_ORANGE])
			

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
	last_cycle = time.time()
	while not game_over:
		msg = midi_in.get_message()
		if msg:
			print(msg)
			if msg[0][0] == 176:
				midi_out.send_message([176, direction, GREEN_LO])
				direction = msg[0][1]
				midi_out.send_message([176, direction, GREEN_HI])
		now = time.time()
		if now - last_cycle > cycle_duration:
			if direction == UP:
				new_field = ((int(snake[0] / 16) - 1) % 8) * 16 + snake[0] % 16
			elif direction == DOWN:
				new_field = ((int(snake[0] / 16) + 1) % 8) * 16 + snake[0] % 16
			elif direction == LEFT:
				new_field = int(snake[0] / 16) * 16 + ((snake[0] % 16) - 1) % 8
			elif direction == RIGHT:
				new_field = int(snake[0] / 16) * 16 + ((snake[0] % 16) + 1) % 8
			if new_field in snake:
				game_over = True
				midi_out.send_message([144, new_field, RED_HI])
			else:
				midi_out.send_message([144, new_field, BRIGHT_ORANGE])
				snake.insert(0,new_field)
			for i in range(len(snake) - snake_length):
				midi_out.send_message([144, snake.pop(), 0])
			if new_field == goodie:
				goodie = -1
				snake_length += 1
			if goodie_in <= 0:
				found = False
				while not found:
					x = int(random.random() * 8)
					y = int(random.random() * 8)
					goodie = y * 16 + x
					found = goodie not in snake
				midi_out.send_message([144, goodie, RED_MI])
				goodie_in = int(random.random() * 10) + 5
			if goodie < 0:
				goodie_in -= 1
			last_cycle = now
		time.sleep(0.0001)
except KeyboardInterrupt:
    print('')
finally:
	time.sleep(3)
	print("Exit.")
	update_all(0)
	midi_in.close_port()
	midi_out.close_port()
	del midi_in
	del midi_out

#			if message[0] == 144:
#				with midi_out:
#					midi_out.send_message([144, message[1], RORANGE_HI]])