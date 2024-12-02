#include <Servo.h>

// Create servo objects
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

// Servo pins
const int SERVO_PINS[] = {3, 5, 6, 9, 10};

void setup() {
  // Attach servos to pins
  servo1.attach(SERVO_PINS[0]);
  servo2.attach(SERVO_PINS[1]);
  servo3.attach(SERVO_PINS[2]);
  servo4.attach(SERVO_PINS[3]);
  servo5.attach(SERVO_PINS[4]);
  
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 5) {  // Wait for 5 characters (one for each servo)
    // Read control string for all servos
    String controlStr = Serial.readStringUntil('\n');
    
    // Control each servo based on its corresponding value
    if (controlStr.length() >= 5) {
      // Servo 1
      servo1.write(controlStr.charAt(0) == '1' ? 90 : 0);
      // Servo 2
      servo2.write(controlStr.charAt(1) == '1' ? 90 : 0);
      // Servo 3
      servo3.write(controlStr.charAt(2) == '1' ? 90 : 0);
      // Servo 4
      servo4.write(controlStr.charAt(3) == '1' ? 90 : 0);
      // Servo 5
      servo5.write(controlStr.charAt(4) == '1' ? 90 : 0);
    }
    
    // Wait for 5 seconds before next command
    delay(5000);
  }
}