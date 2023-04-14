

/*
Example sketch for interfacing with the DS1620 temperature chip.

Copyright (c) 2011, Matt Sparks
All rights reserved.
*/

#include <PoolCom.h>
#include <stdlib.h>
// #include <DS1620.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Temperature Sensors Definitions
#define AIR_TEMP_SENS 8    // Air Temperature Sensor
#define WATER_TEMP_SENS 2    // Water Temperature Sensor

// Water Level Sensor
#define WATER_SENSOR 3    //Water Level Sensor

// Relays
#define RELAY_1 4    // Relay 1
#define RELAY_2 5    // Relay 2
#define RELAY_3 6    // Relay 3
#define RELAY_4 7    // Relay 4

// PH Sensor
#define SensorPin A0            //pH meter Analog output to Arduino Analog Input 0
#define Offset -3.11            //deviation compensate
#define LED 13
#define samplingInterval 20
#define printInterval 800
#define ArrayLength  40    //times of collection
int pHArray[ArrayLength];   //Store the average value of the sensor feedback
int pHArrayIndex=0;
int pHInitializationIndex=0;

// Temperature Sentor Variables
OneWire oneWireA(AIR_TEMP_SENS);
OneWire oneWireW(WATER_TEMP_SENS);
DallasTemperature sensorAir(&oneWireA);
DallasTemperature sensorWater(&oneWireW);

String waterLevel;

float Celcius=0;
float Fahrenheit=0;

int relay;

PoolCom poolCom(9600);

void setup()
{
  Serial.begin(9600); // Baud rate
  delay(100);

  /*
  sensorWater.begin();
  sensorAir.begin();
  */

  pinMode(WATER_SENSOR, INPUT);
  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  pinMode(RELAY_4, OUTPUT);
  // pinMode(LED,OUTPUT);  
  // Serial.println("pH meter experiment!");    //Test the serial monitor
}


void loop()
{
  if(poolCom.read()){
    if(poolCom.getReqType()==0){
      poolCom.write(6);
      /*
      switch(poolCom.getDevice()){
        
        case 0:   
          Celcius=sensorAir.getTempCByIndex(0);
          Fahrenheit=sensorAir.toFahrenheit(Celcius);
          poolCom.write(Fahrenheit);
          break;
        case 1:
          Celcius=sensorWater.getTempCByIndex(0);
          Fahrenheit=sensorWater.toFahrenheit(Celcius);
          poolCom.write(Fahrenheit);
          break;
        case 2:
          poolCom.write(7);//displayPHLevel());
        break;
        case 3:
          poolCom.write((float)digitalRead(WATER_SENSOR));
          break;
          /*
        case 10:   
          poolCom.write(digitalRead(RELAY_1));
          break;
        case 11:
          poolCom.write(digitalRead(RELAY_2));
          break;
        case 12:
          poolCom.write(digitalRead(RELAY_3));
          break;
        case 13:
          poolCom.write(digitalRead(RELAY_4));
          break;
      }
      */
    } // end if req = 0
    /*
    else{
      switch(poolCom.getDevice()){
        case 10:   
          digitalWrite(RELAY_1,poolCom.getData());
          break;
        case 11:
          digitalWrite(RELAY_2,poolCom.getData());
          break;
        case 12:
          digitalWrite(RELAY_3,poolCom.getData());
          break;
        case 13:
          digitalWrite(RELAY_4,poolCom.getData());
          break;
      
      }
      poolCom.write(0)
    } 
    */
  } // end if read
  
  
  
  /*
  displayPHLevel();  
  displayTemperatures();
  displayWaterLevel();
  
  relay = (relay + 1)%1;
  digitalWrite(RELAY_1, relay);
  digitalWrite(RELAY_2, relay);
  digitalWrite(RELAY_3, relay);
  digitalWrite(RELAY_4, relay);
  delay(1000);
  */
  
} // end loop

float displayTemperatures(){
  Serial.println("Water Temperature");
  sensorWater.requestTemperatures(); 
  Celcius=sensorWater.getTempCByIndex(0);
  Fahrenheit=sensorWater.toFahrenheit(Celcius);
  Serial.print(" C  ");
  Serial.print(Celcius);
  Serial.print(" F  ");
  Serial.println(Fahrenheit);
  
  Serial.println("Air Temperature");
  sensorAir.requestTemperatures(); 
  Celcius=sensorAir.getTempCByIndex(0);
  Fahrenheit=sensorAir.toFahrenheit(Celcius);
  Serial.print(" C  ");
  Serial.print(Celcius);
  Serial.print(" F  ");
  Serial.println(Fahrenheit);
}

void displayWaterLevel(){
  waterLevel = " ";
  if(digitalRead(WATER_SENSOR))
     waterLevel = "Low";
  else
     waterLevel = "High";
  Serial.println("Water Level");
  Serial.println(" "+ waterLevel);
}

float displayPHLevel(){
  static unsigned long samplingTime = millis();
  static unsigned long printTime = millis();
  static float pHValue,voltage;
  if(millis()-samplingTime > samplingInterval)
  {
      pHArray[pHArrayIndex++]=analogRead(SensorPin);
      /// Serial.println(analogRead(SensorPin)); for analog pin testing
      if(pHArrayIndex==ArrayLength)pHArrayIndex=0;
      voltage = avergearray(pHArray, ArrayLength)*5.0/1024;
      pHValue = 3.5*voltage+Offset;
      samplingTime=millis();
  }
  if(millis() - printTime > printInterval)   //Every 800 milliseconds, print a numerical, convert the state of the LED indicator
  {
    //Serial.println("PH");
    if(pHInitializationIndex>ArrayLength){
      /*
      Serial.print("Voltage:");
          Serial.print(voltage,2);
          Serial.print("    pH value: ");
      Serial.println(pHValue,2);
          digitalWrite(LED,digitalRead(LED)^1);
          printTime=millis();
      */
      //Serial.println(pHValue,2);
      return pHValue;
    }
    else{
      pHInitializationIndex++;
      //Serial.println(" Uninitialized");
      return -1;
    }
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

