#include <AccelStepper.h>

/*  Project: Code for controlling XY positioning table for tactile sensor testing
    Name: Aiden Shaevitz
    Date: 3/31/2022
*/

const int switch_pin_x = 2;
const int switch_pin_y = 3;

bool switch_x_1 = false;
bool switch_x_2 = false;
bool switch_y_1 = false;
bool switch_y_2 = false;


const float screw_lead = 8; // mm/rotation
const float stepsPerRevolutionXY = 800;  // change this to fit the number of steps per revolution
float current_pos[] = {3.0, 3.0}; // Set very high so that when homing it will always reach the true zero position

// Initialize the stepper library on pins 8 through 12:
AccelStepper stepperX(AccelStepper::DRIVER, 7, 6);
AccelStepper stepperY(AccelStepper::DRIVER, 9, 10);
AccelStepper stepperZ(AccelStepper::DRIVER, 12, 11);

void setup() {
  // initialize the serial port:
  Serial.begin(9600);
  while (!Serial);
  Serial.println("serial started");
  
  // set stepper parameters
  stepperX.setMaxSpeed(200.0);
  stepperX.setAcceleration(100.0);

  stepperY.setMaxSpeed(200.0);
  stepperY.setAcceleration(100.0);
  Serial.println("finished init");

  // Setup interrupts for limit switches
  pinMode(18, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
  pinMode(20, INPUT_PULLUP);
  pinMode(21, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(18), limit_switch_x1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), limit_switch_x2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(20), limit_switch_y1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), limit_switch_y2, CHANGE);

  delay(5);
  
  test();
}

void loop() {
  // put your main code here, to run repeatedly:

}


void test(){
  stepperX.setCurrentPosition(0);
  float pos[2] = {1.0, 1.0};
  moveToPos(pos);
//  bool move_status_x = 1;
  
//  while (move_status_x!=0) {
//    move_status_x = stepperX.run();
//    Serial.println(move_status_x); 
//}
}

// Get number of steps needed to move a certain distance along x or y axis
int getStepsXY(float distance) {
  int steps = round(distance / (screw_lead / stepsPerRevolutionXY));
  Serial.print("number of steps "); Serial.println(steps);
  return steps;
}

void moveToPos(float next_pos[2]) {
  float dX = next_pos[0];
  float dY = next_pos[1];

  int steps_x = getStepsXY(dX);
  int steps_y = getStepsXY(dY);

  stepperX.move(steps_x);
  stepperY.move(steps_y);

  bool move_status_x = 1;
  bool move_status_y = 1;

  while (move_status_x!=0) {
//     check if limit switch tripped
    Serial.println(switch_x_1);
    if (switch_x_1) {
      earlyTermination();
    }
    Serial.println("in step loop");
    move_status_x = stepperX.run();
    Serial.println(move_status_x);
  }
}

void earlyTermination() {
  stepperX.stop();
  stepperY.stop();
  while (true) {
    stepperX.run();
    stepperY.run();
    Serial.println('Early termination triggered, please reset');
  }
}

void limit_switch_x1() {
  static unsigned long last_interrupt_time_x1 = 0;
  unsigned long interrupt_time_x1 = millis();
  interrupt_time_x1 = millis();
  if (interrupt_time_x1 - last_interrupt_time_x1 > 50)
  {
    delay(1);
    int val = digitalRead(18);
    if (val) {
      switch_x_1 = true;
      Serial.println("18 True");
    }
    else if (!val) {
      switch_x_1 = false;
      Serial.println("18 False");
    }

  }
  last_interrupt_time_x1 = interrupt_time_x1;
}

void limit_switch_x2() {
  static unsigned long last_interrupt_time_x2 = 0;
  unsigned long interrupt_time_x2 = millis();
  interrupt_time_x2 = millis();
  if (interrupt_time_x2 - last_interrupt_time_x2 > 50)
  {
    delay(1);
    int val = digitalRead(19);
    if (val) {
      switch_x_2 = true;
      Serial.println("19 True");
    }
    else if (!val) {
      switch_x_2 = false;
      Serial.println("19 False");
    }

  }
  last_interrupt_time_x2 = interrupt_time_x2;
}

void limit_switch_y1() {
  static unsigned long last_interrupt_time_y1 = 0;
  unsigned long interrupt_time_y1 = millis();
  interrupt_time_y1 = millis();
  if (interrupt_time_y1 - last_interrupt_time_y1 > 50)
  {
    delay(1);
    int val = digitalRead(20);
    if (val) {
      switch_y_1 = true;
      Serial.println("20 True");
    }
    else if (!val) {
      switch_y_1 = false;
      Serial.println("20 False");
    }

  }
  last_interrupt_time_y1 = interrupt_time_y1;
}

void limit_switch_y2() {
  static unsigned long last_interrupt_time_y2 = 0;
  unsigned long interrupt_time_y2 = millis();
  interrupt_time_y2 = millis();
  if (interrupt_time_y2 - last_interrupt_time_y2 > 50)
  {
    delay(1);
    int val = digitalRead(21);
    if (val) {
      switch_y_2 = true;
      Serial.println("21 True");
    }
    else if (!val) {
      switch_y_2 = false;
      Serial.println("21 False");
    }

  }
  last_interrupt_time_y2 = interrupt_time_y2;
}
