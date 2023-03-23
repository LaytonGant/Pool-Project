void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Initialize variables
  String msg;
  
  // See if data is available on the serial port
  if (Serial.available()) {
    // Read in data
    msg = Serial.readString();
    // Trim leading or trailing whitespace
    msg.trim();
    // See if message matches
    if (msg == "Hello from Pi!") {
      // Flash LED
      digitalWrite(LED_BUILTIN, HIGH);
      delay(250);
      digitalWrite(LED_BUILTIN, LOW);
      delay(250);
    }
  }
}
