#!/bin/python3

# Necessary imports for the 3 types of components used
from gpiozero import LED, Button, TonalBuzzer
from gpiozero.tones import Tone

# In theory I don't actually need both of these, but they serve different functions here
from signal import pause
from time import sleep

# Defining I/O pins, we're using the cluster of 22-24 for the buttons, 4 for the LED, and 18 for the buzzer which I've since learned is ill-advised
led = LED(4)
recButton = Button(22)
upButton = Button(23)
nextButton = Button(24)
buz = TonalBuzzer(18)

# State trackers for the overall application
recording = False
playing = False

# State trackers for the function so that the While loop doesn't break everything and I don't need to use pause()
runROnce = True
runUOnce = True
runNOnce = True

# Current note and array/list of notes in our 'composition'
note = 60
notes = []

# The record function, really just a state machine manipulator
def rec():
	# all functions have a state tracker up top so they aren't called repeatedly from while()
	global runROnce
	if not runROnce:
		return
	else :
		global recording
		recording = not recording
		if recording:
			led.on()
			notes.clear()
		else :
			led.off()
		print(recording)
		runROnce = False

# This function is for incrementing the note we're currently on, upwards
def up():
	global runUOnce
	if not runUOnce:
		return
	else :
		global note
		if note < 71:
			if note == 64:
				note = note + 1
			else :
				note = note + 2
		else :
			note = 60
		print(note)
		buz.play(Tone(note))
		sleep(0.1)
		buz.stop()
		runUOnce = False

# This simple looking function is where the magic happens - it pushes notes into the array and functions as the play button, and manages tail state
def nxt():
	global runNOnce
	if not runNOnce:
		return
	else :
		global note
		global notes
		global recording
		global playing
		if recording:
			notes.append(note)
			note = 60
		else :
			playing = not playing
		print("Next")
		runNOnce = False

# This just keeps track of the current note being played, if we're playing the composition
currentNote = 0


while True:
	# This loops through the note array playing the song if we're in the play state
	if playing:
		if currentNote < len(notes):
			buz.play(Tone(notes[currentNote]))
			sleep(0.5)
			buz.stop()
			currentNote = currentNote + 1
		else :
			currentNote = 0

	# This is the button logic, it calls the appropriate function based on which button/buttons are pressed, and resets the state trackers
	if recButton.is_pressed:
		rec()
	else :
		runROnce = True
	if upButton.is_pressed:
		up()
	else :
		runUOnce = True
	if nextButton.is_pressed:
		nxt()
	else :
		runNOnce = True

