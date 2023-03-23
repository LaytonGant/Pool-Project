#include "PoolCom.h"

PoolCom a;

void setup() {
  // put your setup code here, to run once:
  a.init(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  a.test();
  delay(500);
}
