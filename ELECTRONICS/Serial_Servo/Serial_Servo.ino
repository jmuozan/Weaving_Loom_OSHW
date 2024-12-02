#include <Servo.h>

// Constants
const int NUM_SERVOS = 5;
const int SERVO_PINS[] = {3, 5, 6, 9, 10};
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 90;
const unsigned long MOVEMENT_DELAY = 5000; // 5 seconds in milliseconds

// Array to store servo objects
Servo servos[NUM_SERVOS];

void setup() {
    Serial.begin(9600);
    
    // Initialize all servos using array
    for (int i = 0; i < NUM_SERVOS; i++) {
        servos[i].attach(SERVO_PINS[i]);
        servos[i].write(MIN_ANGLE);  // Set initial position
    }
    
    Serial.println("Servo Control Ready");
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        processCommand(command);
    }
}

void processCommand(String command) {
    // Extract motor number and value
    int motorNum = command.substring(5, 6).toInt();  // Get number after "motor"
    int value = command.substring(command.indexOf(' ') + 1).toInt();
    
    // Validate input
    if (motorNum < 1 || motorNum > NUM_SERVOS) {
        Serial.println("Invalid motor number. Use 1-5");
        return;
    }
    
    if (value != 0 && value != 1) {
        Serial.println("Invalid value. Use 0 or 1");
        return;
    }
    
    // Move servo
    int angle = value ? MAX_ANGLE : MIN_ANGLE;
    servos[motorNum - 1].write(angle);
    
    // Feedback
    Serial.print("Motor ");
    Serial.print(motorNum);
    Serial.print(" moved to ");
    Serial.print(angle);
    Serial.println(" degrees");
    
    delay(MOVEMENT_DELAY);
}