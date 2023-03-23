/*
    PoolCom.h
    Author: Colin McBride
    Date: March 23 2023
    Version: 1.0

    A library for sending and receiving commands from a Raspberry Pi 
    for a pool controller. 

    ==========Version History==========
    1.0: Created header - March 23 2023
*/

#ifndef PoolCom_h
#define PoolCom_h
#include "Arduino.h"

class PoolCom {
  public:
    PoolCom();
    void init(int baud);
    void test();
  private:
    
};
#endif
