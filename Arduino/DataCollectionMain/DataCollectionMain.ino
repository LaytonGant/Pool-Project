/*
Example sketch for interfacing with the DS1620 temperature chip.

Copyright (c) 2011, Matt Sparks
All rights reserved.
*/


#include <stdlib.h>
#include <DS1620.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

 float Celcius=0;
 float Fahrenheit=0;


// Set the appropriate digital I/O pin connections.
// See the datasheet f  qor more details.
static const uint8_t RST_PIN = 7;  // pin 3 on DS1620
static const uint8_t CLK_PIN = 8;  // pin 2 on DS1620
static const uint8_t DQ_PIN  = 9;  // pin 1 on DS1620


DS1620 ds1620(RST_PIN, CLK_PIN, DQ_PIN);

void setup()
{

  Serial.begin(9600); // Baud rate
  delay(100);

  ds1620.config();

  Serial.begin(9600);
  sensors.begin();
}


void loop()
{

  const float temp_c = ds1620.temp_c();
  const float temp_f = temp_c * 9/5.0 + 32;

  Serial.println("Air Temp");
  Serial.print(" C  ");
  Serial.print(temp_c, 1);
  Serial.print(" F  ");
  Serial.println(temp_f, 1);  // 1 decimal place

  Serial.println("Water Temp");
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Fahrenheit=sensors.toFahrenheit(Celcius);
  Serial.print(" C  ");
  Serial.print(Celcius);
  Serial.print(" F  ");
  Serial.println(Fahrenheit);
  delay(1000);
}
