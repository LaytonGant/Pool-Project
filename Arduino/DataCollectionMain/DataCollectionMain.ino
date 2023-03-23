/*
Example sketch for interfacing with the DS1620 temperature chip.

Copyright (c) 2011, Matt Sparks
All rights reserved.
*/


#include <stdlib.h>
// #include <DS1620.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define AIR_TEMP_SENS 1    // Air Temperature Sensor
#define WATER_TEMP_SENS 2    // Water Temperature Sensor
#define WATER_SENSOR 3    //Water Level Sensor

#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset -.61            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLenth  40    //times of collection
int pHArray[ArrayLenth];   //Store the average value of the sensor feedback
int pHArrayIndex=0;

OneWire oneWire(AIR_TEMP_SENS);
OneWire oneWire(WATER_TEMP_SENS);


DallasTemperature sensors(&oneWire);

 float Celcius=0;
 float Fahrenheit=0;


// Set the appropriate digital I/O pin connections.
// See the datasheet f  qor more details.
static const uint8_t RST_PIN = 5;  // pin 3 on DS1620
static const uint8_t CLK_PIN = 6;  // pin 2 on DS1620
static const uint8_t DQ_PIN  = 7;  // pin 1 on DS1620


DS1620 ds1620(RST_PIN, CLK_PIN, DQ_PIN);

void setup()
{
  Serial.begin(9600); // Baud rate
  delay(100);

  //ds1620.config();

  sensors.begin();

  pinMode(WATER_SENSOR, INPUT);

  pinMode(LED,OUTPUT);
  Serial.begin(9600);
  Serial.println("pH meter experiment!");    //Test the serial monitor
}


void loop()
{
  /*
  const float temp_c = ds1620.temp_c() / 11;
  const float temp_f = temp_c * 9/5.0 + 32;

  Serial.println("Air Temp");
  Serial.print(" C  ");
  Serial.print(temp_c, 1);
  Serial.print(" F  ");
  Serial.println(temp_f, 1);  // 1 decimal place
  */

  Serial.println("Water Temp");
  sensors.requestTemperatures(); 
  Celcius=sensors.getTempCByIndex(0);
  Fahrenheit=sensors.toFahrenheit(Celcius);
  Serial.print(" C  ");
  Serial.print(Celcius);
  Serial.print(" F  ");
  Serial.println(Fahrenheit);

  Serial.println(digitalRead(WATER_SENSOR));
  
  delay(1000);

  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      /// Serial.println(analogRead(SensorPin)); for analog pin testing
      if(pHArrayIndex==ArrayLenth)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLenth)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  if(millis() - printTime > printInterval)   //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
    Serial.print("Voltage:");
        Serial.print(voltage,2);
        Serial.print("    pH value: ");
    Serial.println(pHValue,2);
        digitalWrite(LED,digitalRead(LED)^1);
        printTime=millis();
  }
}

double avergearray(int* arr, int number){
  int i;
  int max,min;
  double avg;
  long amount=0;
  if(number<=0){
    Serial.println("Error number for the array to avraging!/n");
    return 0;
  }
  if(number<5){   //less than 5, calculated directly statistics
    for(i=0;i<number;i++){
      amount+=arr[i];
    }
    avg = amount/number;
    return avg;
  }else{
    if(arr[0]<arr[1]){
      min = arr[0];max=arr[1];
    }
    else{
      min=arr[1];max=arr[0];
    }
    for(i=2;i<number;i++){
      if(arr[i]<min){
        amount+=min;        //arr<min
        min=arr[i];
      }else {
        if(arr[i]>max){
          amount+=max;    //arr>max
          max=arr[i];
        }else{
          amount+=arr[i]; //min<=arr<=max
        }
      }//if
    }//for
    avg = (double)amount/(number-2);
  }//if
  return avg;
}
