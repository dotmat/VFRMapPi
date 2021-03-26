// VFR Sectional Map with LEDs
// Mathew Jenkinson March 2021

// This script is currently unfinished but is the NodeJS port of the metarManager.py 

'use-strict';
const get = require('simple-get')
var Gpio = require('onoff').Gpio;
console.log("Welcome to Mats Aviation Map Metar Pi.");
const apiKey = "";

const airports = {'KPDK':(19,21,23),'KRYY':(11,13,15),'KLZU':(33,35,37),'KPUJ':(3,5,7),'KATL':(36,38,40)};
var flightRulesObject = {};

function getMetar(airportCode){
    //console.log('Getting METAR on '+airportCode);
    const opts = {
        method: 'GET',
        url: 'https://avwx.rest/api/metar/'+airportCode+'?format=json',
        headers: {
            "Authorization": apiKey
        },
        json: true
    };
    get.concat(opts, function (err, res, data) {
        if(err){
            // If we cant get the weather then mark the value as dead so the LED is not illumiated. 
            flightRulesObject[airportCode]= "INVALID";
        }
        //console.log(data) // `data` is an object
        if(data.flight_rules){
            //console.log(data["flight_rules"]);
            flightRulesObject[airportCode] = data["flight_rules"];
        }
        
        // If the number of flight rules matches the number of airports then call the function to update the lights.
        if(Object.keys(airports).length == Object.keys(flightRulesObject).length){
            console.log('Got all the data for our airports, here are the details;');
            console.log(flightRulesObject);
            updateLEDsWithMETAR();
        }
    });
};

function updateLEDsWithMETAR(){
    // METAR information is represented as
    // VFR == green
    // MVFR == blue
    // IFR == red
    // LIFR == purple
    // Invalid == off

}

function resetLEDs(){
    // Reset function flashes each red green blue purple cycle twice
    console.log('Resetting LEDs');
    LED.writeSync(1);
    return Promise.resolve("Success");
}

const LED = new Gpio(36, 'out');
resetLEDs().then((message) => {
        Object.keys(airports).forEach(airportID => {
            getMetar(airportID);
        });
    }
);


