#include "PoolCom.h"

PoolCom poolCom(9600);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  poolCom.init();
  poolCom.test();
}

void loop() {
  if (poolCom.read()) {
    if (poolCom.getReqType() == 2) {
      flashLED();
    }
    if (poolCom.getDevice() == 3) {
      flashLED();
    }
    if (poolCom.getData() == 1) {
      flashLED();
    }
    poolCom.write(1);
  }
  else {
    poolCom.write(0);
  }
  delay(1000);
}

void flashLED() {
  digitalWrite(LED_BUILTIN,HIGH);
  delay(250);
  digitalWrite(LED_BUILTIN,LOW);
  delay(250);
}
