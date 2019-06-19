
#include <Wire.h>
#include "TSL2561.h"
#include "DHT.h"

#define DHTPIN 12     // what digital pin we're connected to

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

DHT dht(DHTPIN, DHTTYPE);
String L = "L";
String T = "T";
String bracket = ")";
// Example for demonstrating the TSL2561
// connect SCL to analog 5
// connect SDA to analog 4
// connect VDD to 3.3V DC
// connect GROUND to common ground
TSL2561 tsl(TSL2561_ADDR_FLOAT); 

uint16_t getLux();

void setup() {
  Serial.begin(9600);
  
  if (tsl.begin()) {
    //Serial.println("Found tsl sensor");
  } else {
    //Serial.println("No tsl sensor?");
    while (1);
  }
  // You can change the gain on the fly, to adapt to brighter/dimmer light situations
  //tsl.setGain(TSL2561_GAIN_0X);         // set no gain (for bright situtations)
  tsl.setGain(TSL2561_GAIN_16X);      // set 16x gain (for dim situations)

  // Changing the integration time gives you a longer time over which to sense light
  // longer timelines are slower, but are good in very low light situtations!
  tsl.setTiming(TSL2561_INTEGRATIONTIME_13MS);  // shortest integration time (bright light)
  //tsl.setTiming(TSL2561_INTEGRATIONTIME_101MS);  // medium integration time (medium light)
  //tsl.setTiming(TSL2561_INTEGRATIONTIME_402MS);  // longest integration time (dim light)

  dht.begin();
}

void loop() {
//一行print
  // get lux

  
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

   // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("f");
    return;
  }
  
  while(Serial.available()>0){
    char r = Serial.read();
    if(r == 'l'){
      uint16_t lux = getLux();
      String sL = "(" + L + lux + ")";
      Serial.println(sL);
      break;
    }
    if(r == 't'){
      String sT = "(" + T + t + ")";
      Serial.println(sT);
      break;
    }
  }
}

uint16_t getLux(){
  //Read 32 bits with top 16 bits IR, bottom 16 bits full spectrum
  uint32_t lum = tsl.getFullLuminosity();
  uint16_t ir, full;
  ir = lum >> 16;
  full = lum & 0xFFFF;
  return tsl.calculateLux(full, ir);
}

