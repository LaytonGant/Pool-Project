void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Initialize variables
  String strMsg;
  int intMsg;
  
  // See if data is available on the serial port
  if (Serial.available()) {
    // Read in data
    intMsg = readInt();
    
    // See if message matches
    if (intMsg == 23) {
      // Flash LED
      digitalWrite(LED_BUILTIN, HIGH);
      delay(250);
      digitalWrite(LED_BUILTIN, LOW);
      delay(250);
    }
  }
}

String readStr() {
  String msg;
  
  // Read in data
  msg = Serial.readString();
  // Trim leading or trailing whitespace
  msg.trim();

  return msg;
}

int readInt() {
  int msg;
  
  // Read in data
  msg = Serial.parseInt();

  return msg;
}
