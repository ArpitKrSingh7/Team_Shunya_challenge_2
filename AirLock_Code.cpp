#include <Arduino.h>

// Sensor & Gate Pins
#define PRESENCE_FRONT 4
#define PRESENCE_BACK 5
#define PRESENCE_MIDDLE 13 
#define GATE_SAFETY_A 14
#define GATE_SAFETY_B 16
#define GATE_MOVING_A 17
#define GATE_MOVING_B 18

#define GATE_REQUEST_A 2 //Onboard LED
#define GATE_REQUEST_B 22

// Track gate output states
bool gate_request_state_A = LOW;
bool gate_request_state_B = LOW;

void setup() {
    Serial.begin(115200);

    // Sensor Pins - Inputs
    pinMode(PRESENCE_FRONT, INPUT);
    pinMode(PRESENCE_BACK, INPUT);
    pinMode(PRESENCE_MIDDLE, INPUT);
    pinMode(GATE_SAFETY_A, INPUT);
    pinMode(GATE_SAFETY_B, INPUT);
    pinMode(GATE_MOVING_A, INPUT);
    pinMode(GATE_MOVING_B, INPUT);

    // Gate control pins - Outputs
    pinMode(GATE_REQUEST_A, OUTPUT);
    pinMode(GATE_REQUEST_B, OUTPUT);

    // Ensure gates are closed at startup
    gate_request_state_A = LOW;
    gate_request_state_B = LOW;
    digitalWrite(GATE_REQUEST_A, gate_request_state_A);
    digitalWrite(GATE_REQUEST_B, gate_request_state_B);
}

void loop() {
    // Read inputs
    bool presence_front = 1; // 1, 0, 0
    bool presence_back = 1;
    bool presence_middle = 1;
    bool gate_safety_A = 1;
    bool gate_safety_B = 1;
    bool gate_moving_A = 1;
    bool gate_moving_B = 1;

    // ROVER IS IN FRONT — Open Gate A if it's safe
    if (presence_front && !gate_safety_A && !gate_moving_A) {
        gate_request_state_A = HIGH;  // Request to open gate A
        gate_request_state_B = LOW;   // Ensure gate B stays closed
    }

    // ROVER IS IN MIDDLE AND GATE A IS OPEN — Close both gates
    if (presence_middle && gate_request_state_A && !gate_safety_A && !gate_moving_A && !gate_moving_B) {
        gate_request_state_A = LOW;
        gate_request_state_B = LOW;
    }

    // ROVER IS IN MIDDLE AND BOTH GATES ARE CLOSED — Open Gate B
    if (presence_middle && !gate_request_state_A && !gate_request_state_B && !gate_moving_A && !gate_moving_B) {
        gate_request_state_A = LOW;
        gate_request_state_B = HIGH;
    }

    // ROVER IS AT BACK — Close all gates
     if (presence_back && !gate_safety_B && !gate_moving_B) {
        gate_request_state_A = LOW;
        gate_request_state_B = LOW;
    }

    // Apply the new gate states
    digitalWrite(GATE_REQUEST_A, gate_request_state_A);
    digitalWrite(GATE_REQUEST_B, gate_request_state_B);

    delay(100);  // Optional: reduce CPU usage
}