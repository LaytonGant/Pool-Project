/*
    PoolCom.cpp
    Author: Colin McBride
    Date: March 23 2023
    Version: 1.0

    A library for sending and receiving commands from a Raspberry Pi 
    for a pool controller. 

*/

#include "Arduino.h"
#include "PoolCom.h"

// Constructor with baud rate specified
PoolCom::PoolCom(int b) {
  // Set initial values
  baud = b;
  goodRead = false;
  reqType = -1;
  device = -1;
  data = -1;
}

// Initialize communication
void PoolCom::init() {
  Serial.begin(baud);
}

// A simple test function
void PoolCom::test() {
  Serial.println("This is a test function.");
}

// Reads and parses a message. 
// Returns true if a message was successfully received, false otherwise. 
// If a message is not successfully received, no class attributes are overwritten. 
bool PoolCom::read() {
  // Initialize local variables
  int msg[3];

  // Read in data or return if no successful read
  goodRead = true;
  for (int i = 0; i < 3; i++) {
    if (Serial.available()) {
      msg[i] = Serial.parseInt();
    }
    else {
      goodRead = false;
      return false;
    }
  }

  // Write new data to class attributes
  reqType = msg[0];
  device = msg[1];
  data = msg[2];

  // Message received
  return true;
}

// Writes a message. 
// Returns false if a message cannot be successfully sent, true otherwise. 
bool PoolCom::write(float msgData) {
  // Initialize local variables
  String msg;

  // Parse message data to string
  msg = String(msgData);

  // Try to send message
  if (Serial.availableForWrite() > 0) {
    Serial.println(msg);
    return true;
  }
  else {
    return false;
  }
}


/*
 * ------ GETTERS AND SETTERS ------
 */
int PoolCom::getBaud() {
  return baud;
}

bool PoolCom::isGoodRead() {
  return goodRead;
}

int PoolCom::getReqType() {
  return reqType;
}

int PoolCom::getDevice() {
  return device;
}

int PoolCom::getData() {
  return data;
}
