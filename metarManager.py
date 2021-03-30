#!/usr/bin/env python3

# Live Sectional Metar Map Controller
# Mathew Jenkinson March 2021

import os
import urllib.request
import simplejson as json
import time
import RPi.GPIO as GPIO

apiKey = ""
#apiKey = os.getenv('avwxKey')
flightRulesObject = {}

def getMetar(airportCode):
    url = 'https://avwx.rest/api/metar/'+airportCode+'?format=json'
    hdr = { 'Authorization' : apiKey }
    
    try:
        metarRequest = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(metarRequest)
        metarResponse = response.read().decode('utf-8')
        jsonMetar = json.loads(metarResponse)

        if jsonMetar['flight_rules'] == 'VFR': 
            flightRulesObject[airportCode] = 'GREEN'

        if jsonMetar['flight_rules'] == 'MVFR': 
            flightRulesObject[airportCode] = 'BLUE'

        if jsonMetar['flight_rules'] == 'IFR': 
            flightRulesObject[airportCode] = 'RED'

        if jsonMetar['flight_rules'] == 'LIFR': 
            flightRulesObject[airportCode] = 'PURPLE'

        # flightRulesObject[airportCode] = jsonMetar['flight_rules']

        if len(flightRulesObject) == len(ledPins):
            print(flightRulesObject)
            # Send a Message to PubNub with the Metar data
            flightRulesString = json.dumps(flightRulesObject)
            #print(urllib.parse.quote(flightRulesString))
            pubnubURL = 'https://ps.pndsn.com/publish/pn-key/pn-subkey/0/mapPi/myCallback/'+urllib.parse.quote(flightRulesString)+'?store=0&uuid=MatsMapPi'

            with urllib.request.urlopen(pubnubURL) as response:
                print("Message Sent to PubNub")
            updateLEDsFromMETARs()


    except e:
        print(e)
        flightRulesObject[airportCode] = 'OFF'

def allLEDs(color):
    for led in ledPins:
        setLED(led, color)

def setLED(ledLocation, color):
  ledPWMMatrix[ledLocation]['RED'].ChangeDutyCycle(colors[color][0])
  ledPWMMatrix[ledLocation]['GREEN'].ChangeDutyCycle(colors[color][1])
  ledPWMMatrix[ledLocation]['BLUE'].ChangeDutyCycle(colors[color][2])

def updateLEDsFromMETARs():
    print('Updating LEDS to match METARs')
    for airport in flightRulesObject:
        setLED(airport, flightRulesObject[airport])
    # Sleep for 55 minutes
    time.sleep(3360) 




 
GPIO.setmode(GPIO.BOARD)
pwmFrequency = 100.0
ledPWMMatrix = {}

ledPins = {'KATL':(19,21,23),'KJFK':(11,13,15),'KSFO':(33,35,37),'KMIA':(3,5,7),'KMCO':(36,38,40)}
# ledPins = eval(os.getenv('metarObject'))
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

# Get All the Metars
print('Getting Metars')
for airportCode in ledPins:
    getMetar(airportCode)
