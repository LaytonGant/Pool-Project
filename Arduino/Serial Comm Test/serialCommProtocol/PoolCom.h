/*
    PoolCom.h
    Author: Colin McBride
    Date: March 23 2023
    Version: 1.0

    A library for sending and receiving commands from a Raspberry Pi 
    for a pool controller. 

    ========== VERSIONS ==========
    v1.0 (3/30/23): Created file. Added basic init, read, and write functionality. 
*/

#ifndef PoolCom_h
#define PoolCom_h
#include "Arduino.h"

class PoolCom {
  public:
    PoolCom(int b);
    void init();
    void test();
    bool read();
    bool write(int msgData);

    // Getters and setters
    int getBaud();
    bool isGoodRead();
    int getReqType();
    int getDevice();
    int getData();
  private:
    int baud;     // Communication baud rate
    bool goodRead; // If the last read attempt was successful
    
    // The 3 attributes below are valid only for the last read attempt
    int reqType;  // Request type (input/output)
    int device;   // Target device
    int data;     // Instruction data
    
};

#endif
