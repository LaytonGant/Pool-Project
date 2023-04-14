#include "PoolCom.h"

PoolCom poolCom(9600);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  poolCom.init();
}

void loop() {
  if (poolCom.read()) {
    poolCom.write(1);
    if (poolCom.getReqType() == 2) {
      flashLED();
    }
    if (poolCom.getDevice() == 3) {
      flashLED();
    }
    if (poolCom.getData() == 1) {
      flashLED();
    }
  }
}

void flashLED() {
  digitalWrite(LED_BUILTIN,HIGH);
  delay(250);
  digitalWrite(LED_BUILTIN,LOW);
  delay(250);
}
