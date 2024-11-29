#include <Servo.h>

Servo myservo;
int pos = 0;    

void setup() {
  myservo.attach(9);  
}

void loop() {
  // From 0 to 90 degrees
  for (pos = 0; pos <= 180; pos += 1) {
    myservo.write(pos);
    delay(20);  
  }
  delay(150);

  // From 90 to 0 degrees
  for (pos = 180; pos >= 0; pos -= 1) {
    myservo.write(pos);
    delay(20);  
  }
  delay(150);
}