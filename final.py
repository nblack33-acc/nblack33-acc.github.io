#!/bin/python3

from gpiozero import LED, Button, TonalBuzzer
from gpiozero.tones import Tone
from signal import pause
from time import sleep

led = LED(4)
recButton = Button(22)
upButton = Button(23)
nextButton = Button(24)
buz = TonalBuzzer(18)

recording = False
playing = False
note = 60
notes = []
runROnce = True
runUOnce = True
runNOnce = True

def rec():
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


currentNote = 0

while True:
	if playing:
		if currentNote < len(notes):
			buz.play(Tone(notes[currentNote]))
			sleep(0.5)
			buz.stop()
			currentNote = currentNote + 1
		else :
			currentNote = 0
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

