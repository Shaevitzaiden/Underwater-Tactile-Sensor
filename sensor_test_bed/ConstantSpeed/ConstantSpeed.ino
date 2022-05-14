#include <AccelStepper.h>

bool switch_x_1 = false;
bool switch_x_2 = false;
bool switch_y_1 = false;
bool switch_y_2 = false;

const float screw_lead = 8; // mm/rotation
const float stepsPerRevolutionXY = 800;  // change this to fit the number of steps per revolution
const float stepsPerRevolutionZ = 200;

AccelStepper stepperX(AccelStepper::DRIVER, 7, 6); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperY(AccelStepper::DRIVER, 8, 9); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


void setup()
{
  Serial.begin(9600);
  stepperX.setMaxSpeed(500);
  stepperY.setMaxSpeed(500);

  stepperX.setAcceleration(1000);
  stepperY.setAcceleration(1000);

  pinMode(18, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
  pinMode(20, INPUT_PULLUP);
  pinMode(21, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(20), limit_switch_x1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), limit_switch_x2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(18), limit_switch_y1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), limit_switch_y2, CHANGE);

  // Slightly back off of limit switches if pressed and lift carriage
   startup_motors();

  float pos[2] = {-15., -15.};
  moveToPos(pos);
  //  delay(10000000000000);
}

void loop() {

}

void startup_motors() {
  int sx1 = digitalRead(20);
  int sx2 = digitalRead(21);
  int sy1 = digitalRead(18);
  int sy2 = digitalRead(19);
  Serial.println("startup");
  int ls_dist = getStepsXY(10.0);
  Serial.println(ls_dist);
  if (sy1) {
    stepperY.moveTo(-ls_dist);
    Serial.println("sy1");
  }
  else if (sy2) {
    stepperY.moveTo(ls_dist);
    Serial.println("sy2");
  }
  if (sx1) {
    stepperX.moveTo(-ls_dist);
    Serial.println("sx1");
  }
  else if (sx2) {
    stepperX.moveTo(ls_dist);
    Serial.println("sx1");
  }
  
  int distX = stepperX.distanceToGo();
  int distY = stepperY.distanceToGo();
  Serial.println(distX);
  Serial.println(distY);
  while ((distX != 0)) {
    Serial.println("moving");
    stepperX.run();
    stepperY.run();
    distX = stepperX.distanceToGo();
    distY = stepperY.distanceToGo();
  }
  //  stepperX.setSpeed(0);
  //  stepperX.runSpeed();
}

void moveToPos(float pos[2]) {
  int stepsX = getStepsXY(pos[0]);
  int stepsY = getStepsXY(pos[1]);
  
  stepperX.moveTo(stepsX);
  stepperY.moveTo(stepsY);

  int distX = stepperX.distanceToGo();
  int distY = stepperY.distanceToGo();
  while (distX != 0) {
    if (switch_x_1 || switch_x_2) {
      stepperX.stop();
      while (true) {
        stepperX.run();
        Serial.println("stopping");
      }
    }
    distX = stepperX.distanceToGo();
    stepperX.run();
//    stepperX.setSpeed(200);
  }
  Serial.println("-------------- Finished ----------------");
}

// Get number of steps needed to move a certain distance along x or y axis
int getStepsXY(float distance) {
  int steps = round(distance * stepsPerRevolutionXY / screw_lead );
  return steps;
}


// --------------- LIMIT SWITCH FUNCTIONS ------------------
void limit_switch_x1() {
  static unsigned long last_interrupt_time_x1 = 0;
  unsigned long interrupt_time_x1 = millis();
  interrupt_time_x1 = millis();
  if (interrupt_time_x1 - last_interrupt_time_x1 > 50)
  {
    delay(1);
    int val = digitalRead(20);
    if (val) {
      switch_x_1 = true;
      Serial.println("20 True");
    }
    else if (!val) {
      switch_x_1 = false;
      Serial.println("20 False");
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
    int val = digitalRead(21);
    if (val) {
      switch_x_2 = true;
      Serial.println("21 True");
    }
    else if (!val) {
      switch_x_2 = false;
      Serial.println("21 False");
    }
  }
  last_interrupt_time_x2 = interrupt_time_x2;
}

void limit_switch_y1() {
  static unsigned long last_interrupt_time_y1 = 0;
  unsigned long interrupt_time_y1 = millis();
  interrupt_time_y1 = millis();
  if (interrupt_time_y1 - last_interrupt_time_y1 > 50) {
    delay(1);
    int val = digitalRead(18);
    if (val) {
      switch_y_1 = true;
      Serial.println("18 True");
    }
    else if (!val) {
      switch_y_1 = false;
      Serial.println("18 False");
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
    int val = digitalRead(19);
    if (val) {
      switch_y_2 = true;
      Serial.println("19 True");
    }
    else if (!val) {
      switch_y_2 = false;
      Serial.println("19 False");
    }

  }
  last_interrupt_time_y2 = interrupt_time_y2;
}
