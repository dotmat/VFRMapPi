# Test LED's
# Mathew Jenkinson March 2021

# This Script tests all the LEDs

import RPi.GPIO as GPIO
import time

def allLEDs(color):
    for led in ledPins:
        setLED(led, color)

def setLED(ledLocation, color):
  ledPWMMatrix[ledLocation]['RED'].ChangeDutyCycle(colors[color][0])
  ledPWMMatrix[ledLocation]['GREEN'].ChangeDutyCycle(colors[color][1])
  ledPWMMatrix[ledLocation]['BLUE'].ChangeDutyCycle(colors[color][2])

 
GPIO.setmode(GPIO.BOARD)
pwmFrequency = 100.0
ledPWMMatrix = {}

ledPins = {'KPDK':(19,21,23),'KRYY':(11,13,15),'KLZU':(33,35,37),'KPUJ':(3,5,7),'KATL':(36,38,40)}
colors = {'RED':(20.0,0.0,0.0),'GREEN':(0.0,50.0,0.0),'BLUE':(0.0,0.0,100.0),'PURPLE':(50.0,0.0,50.0), 'OFF':(0.0,0.0,0.0)}


for led in ledPins:
  GPIO.setup(ledPins[led], GPIO.OUT)  

for led in ledPins:
  (redPin, greenPin, bluePin) = ledPins[led]
  ledPWMMatrix[led] = {}
  ledPWMMatrix[led]['RED'] = GPIO.PWM(redPin, pwmFrequency)
  ledPWMMatrix[led]['GREEN'] = GPIO.PWM(greenPin, pwmFrequency)
  ledPWMMatrix[led]['BLUE'] = GPIO.PWM(bluePin, pwmFrequency)
  for color in ledPWMMatrix[led]:
    ledPWMMatrix[led][color].start(0.0)


# Test all the LED's 
print('Going Red')
allLEDs('RED')
time.sleep(2)

print('Going Green')
allLEDs('GREEN')
time.sleep(2)

print('Going Blue')
allLEDs('BLUE')
time.sleep(2)

print('Going Purple')
allLEDs('PURPLE')
time.sleep(2)