#include <AccelStepper.h>

bool switch_x_1 = false;
bool switch_x_2 = false;
bool switch_y_1 = false;
bool switch_y_2 = false;

const float screw_lead = 8; // mm/rotation
const float stepsPerRevolutionXY = 800;
const float stepsPerRevolutionZ = 200;

AccelStepper stepperX(AccelStepper::DRIVER, 7, 6); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperY(AccelStepper::DRIVER, 8, 9); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperZ(AccelStepper::DRIVER, 12, 11); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;
int dataNumber = 0;


void setup()
{
  Serial.begin(115200);
  clearInputBuffer();
  Serial.println("1");
  
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
//  Serial.println(10);
  //  float pos[2] = {5., 20.};
  //  moveToPos_mm(pos);

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
      runDemo();
    }
    newData = false;
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
  Serial.println(2);
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
  moveSteps(steps);

}

void moveToPos_mm(float pos[2]) {
  // convert coords (mm) to steps and round to closest number of steps
  int steps[2] = {getStepsXY(pos[0]), getStepsXY(pos[1])};
  moveSteps(steps);
}

void moveSteps(int steps[2]) {
  // Set position to go to in steps
  stepperX.moveTo(steps[0]);
  stepperY.moveTo(steps[1]);

  // Motor movement loop
  while ((stepperX.distanceToGo() != 0) ||  (stepperY.distanceToGo() != 0)) {
    if (switch_x_1 || switch_x_2 || switch_y_1 || switch_y_2) {
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
//  Serial.println("-------------- Finished ----------------");
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
//      Serial.println("18 True");
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
