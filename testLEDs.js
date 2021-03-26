'use-strict';

var Gpio = require('onoff').Gpio;
var LED = new Gpio(4, 'out'); //use GPIO pin 5 as output
LED.writeSync(1);

