#include <AccelStepper.h>

bool switch_x_1 = false;
bool switch_x_2 = false;
bool switch_y_1 = false;
bool switch_y_2 = false;

const float screw_lead = 8; // mm/rotation
float stepsPerRevolutionXY = 800;
float stepsPerRevolutionZ = 200;

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;
int dataNumber = 0;

AccelStepper stepperX(AccelStepper::DRIVER, 7, 6); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperY(AccelStepper::DRIVER, 8, 9); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperZ(AccelStepper::DRIVER, 12, 11); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5


void setup()
{
  Serial.begin(115200);
  clearInputBuffer();
  Serial.println("10");

  stepperX.setMaxSpeed(400);
  stepperY.setMaxSpeed(400);
  stepperZ.setMaxSpeed(100);

  stepperX.setAcceleration(1000);
  stepperY.setAcceleration(1000);
  stepperZ.setAcceleration(1000);

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
  Serial.println("11");
//  int offset[2] = {};
//  getOffset(offset);
//  moveToHome(offset);
}

void loop() {
  recvWithStartEndMarker();
  parseCommands();
}

void clearInputBuffer() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

void recvWithStartEndMarker() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

void parseCommands() {
  int c[3] = {0, 0, 0};
  int c_idx = 0;
  int t_idx = 0;
  char temp[32];

  if (newData == true) {
    // Parse other values
    int len = strlen(receivedChars);
    for (int i = 0; i < len + 1; i++) {
      if ((receivedChars[i] != ',') && (i != len)) {
        temp[t_idx] = receivedChars[i];
        t_idx++;
      }
      else {
        temp[i] = '\0';
        c[c_idx] = atoi(temp);
        c_idx++;
        t_idx = 0;
      }
    }
    if (c[0] == 0) {
      Serial.println(c[0]);
      while (true);
    }
    else if (c[0] == 1) {
      Serial.println(c[0]);
      //      writeSensorData();
    }
    else if (c[0] == 2) {
      Serial.println(c[0]);
      float coords[2] = {c[1], c[2]};
      moveToPos_mm(coords);
      Serial.println(c[0]);
    }
    else if (c[0] == 3) {
      Serial.println(c[0]);
      int steps[2] = {c[1], c[2]};
      moveSteps(steps, false);
    }
    else if (c[0] == 4) {
      Serial.println(c[0]);
      if (c[1] == 0){
        raiseZ();
      }
      else if (c[1] == 1){
        lowerZ();
      }
      else if (c[1] == 2){
        // do nothing for now, but can add in degree motion of z-axis when I make a function for that
      }
    }
    else if (c[0] == 6) {
      Serial.println(c[0]);
      runToLimitSwitches();
    }
    else if (c[0] == 7) {
      Serial.println(c[0]);
      int homeOffsets[2] = {};
      getOffset(homeOffsets);
      Serial.print(homeOffsets[0]); Serial.print(", "); Serial.println(homeOffsets[1]);
    }
    else if (c[0] == 9) {
      Serial.println(c[0]);
      stepsPerRevolutionXY = c[1];
      stepsPerRevolutionZ = c[2];
    }
    newData = false;
  }
}


void moveToHome(int offset[2]) {
  // First run to limit switches
  offset[0] =  offset[0] * -1;
  offset[1] =  offset[1] * -1;
  moveSteps(offset, true);
}


void runToLimitSwitches() {
  stepperX.setMaxSpeed(200);
  stepperY.setMaxSpeed(200);

  int stepsX = getStepsXY(-100.0);
  int stepsY = getStepsXY(-100.0);

  bool zeroedX = false;
  bool zeroedY = false;

  stepperX.moveTo(stepsX);
  stepperY.moveTo(stepsY);

  while ((!switch_x_2) || (!switch_y_2)) {
    if (switch_x_2 && (!zeroedX)) {
      stepperX.setCurrentPosition(0);
      zeroedX = true;
      stepperX.moveTo(0);
    }
    if (switch_y_2 && (!zeroedY)) {
      stepperY.setCurrentPosition(0);
      zeroedY = true;
      stepperY.moveTo(0);
    }
    stepperX.run();
    stepperY.run();
  }
  // Make sure that it is stopped all of the way

}


void getOffset(int *offsets) {
  stepperX.setMaxSpeed(200);
  stepperY.setMaxSpeed(200);

  // Set position to go to in steps
  int stepsX = getStepsXY(-100.0);
  int stepsY = getStepsXY(-100.0);

  bool zeroedX = false;
  bool zeroedY = false;

  stepperX.moveTo(stepsX);
  stepperY.moveTo(stepsY);

  while ((!switch_x_2) || (!switch_y_2)) {
    if (switch_x_2 && (!zeroedX)) {
      offsets[0] = (int) stepperX.currentPosition();
      stepperX.setCurrentPosition(0);
      zeroedX = true;
      stepperX.moveTo(0);
    }
    if (switch_y_2 && (!zeroedY)) {
      offsets[1] = (int) stepperY.currentPosition();
      stepperY.setCurrentPosition(0);
      zeroedY = true;
      stepperY.moveTo(0);
    }
    stepperX.run();
    stepperY.run();
  }
}


void runDemo() {
  float pos0[2] = {0., 0.};
  float pos1[2] = { -1., -5.};
  float pos2[2] = { -1., -7.};
  float pos3[2] = { -3., -5.};
  float pos4[2] = { -3., -7.};
  raiseZ();
  moveToPos_mm(pos1);
  cycleZ();
  moveToPos_mm(pos2);
  cycleZ();
  moveToPos_mm(pos3);
  cycleZ();
  moveToPos_mm(pos4);
  cycleZ();
  moveToPos_mm(pos0);
  lowerZ();
  lowerZ();
  Serial.println("2");
}

void cycleZ() {
  lowerZ();
  delay(1000);
  raiseZ();
}

void startup_motors() {
  int sx1 = digitalRead(20);
  int sx2 = digitalRead(21);
  int sy1 = digitalRead(18);
  int sy2 = digitalRead(19);

  int ls_steps = getStepsXY(10.0);
  int steps[2] = {0, 0};

  // Check for any triggered limit switches and backoff
  if (sy1) {
    steps[1] = -ls_steps;
  }
  else if (sy2) {
    steps[1] =  ls_steps;
  }
  if (sx1) {
    steps[0] =  -ls_steps;
  }
  else if (sx2) {
    steps[0] =  ls_steps;
  }
  moveSteps(steps, true);

}

void moveToPos_mm(float pos[2]) {
  // convert coords (mm) to steps and round to closest number of steps
  int steps[2] = {getStepsXY(pos[0]), getStepsXY(pos[1])};
  moveSteps(steps, false);
}

void moveSteps(int steps[2], bool ignore_ls) {
  stepperX.setMaxSpeed(400);
  stepperY.setMaxSpeed(400);
  // Set position to go to in steps
  stepperX.moveTo(steps[0]);
  stepperY.moveTo(steps[1]);

  // Motor movement loop
  while ((stepperX.distanceToGo() != 0) ||  (stepperY.distanceToGo() != 0)) {
    if ((switch_x_1 || switch_x_2 || switch_y_1 || switch_y_2) && (!ignore_ls)) {
      stepperX.stop();
      stepperY.stop();
      while (true) {
        stepperX.run();
        stepperY.run();
        //        Serial.println("stopping");
      }
    }
    stepperX.run();
    stepperY.run();
  }
}

void raiseZ() {
  stepperZ.moveTo(150);
  while (stepperZ.distanceToGo() != 0) {
    stepperZ.run();
  }
}

void lowerZ() {
  stepperZ.moveTo(0);
  while (stepperZ.distanceToGo() != 0) {
    stepperZ.run();
  }
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
      //      Serial.println("20 True");
    }
    else if (!val) {
      switch_x_1 = false;
      //      Serial.println("20 False");
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
//      Serial.println("21 True");
    }
    else if (!val) {
      switch_x_2 = false;
//      Serial.println("21 False");
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
      //            Serial.println("18 True");
    }
    else if (!val) {
      switch_y_1 = false;
      //      Serial.println("18 False");
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
//      Serial.println("19 True");
    }
    else if (!val) {
      switch_y_2 = false;
//      Serial.println("19 False");
    }
  }
  last_interrupt_time_y2 = interrupt_time_y2;
}
