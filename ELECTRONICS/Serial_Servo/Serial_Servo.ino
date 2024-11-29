#include <Servo.h>

Servo myservo;
int pos = 0;
int valor;

void setup() {
  myservo.attach(9);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    valor = Serial.parseInt();
    if (valor) {
      myservo.write(90);
    } else {
      myservo.write(0);
    }
    delay(1000);
  }
}