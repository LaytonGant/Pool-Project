/*
    PoolCom.cpp
    Author: Colin McBride
    Date: March 23 2023
    Version: 1.0

    A library for sending and receiving commands from a Raspberry Pi 
    for a pool controller. 

    ==========Version History==========
    1.0: Created file - March 23 2023
*/

#include "Arduino.h"
#include "PoolCom.h"

// Default constructor
PoolCom::PoolCom() {
    
}

// Initialize communicator
void PoolCom::init(int baud) {
    Serial.begin(baud);
}

// A simple test function
void PoolCom::test() {
    Serial.println("This is a test function.");
}
