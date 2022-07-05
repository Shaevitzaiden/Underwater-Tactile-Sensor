#include <AccelStepper.h>
#include "Wire.h"

#define mux_addr 0x70
#define sensor_addr 0x76

#define reset 0x1E
#define adc_read 0x00

#define posr245 0x40
#define posr512 0x42
#define posr1024 0x44  // conversion time approx = 1.88-2.28ms
#define posr2048 0x46
#define posr4096 0x48

#define tosr245 0x50
#define tosr512 0x52
#define tosr1024 0x54  // conversion time approx = 1.88-2.28ms
#define tosr2048 0x56
#define tosr4096 0x58

uint8_t current_channel = 0;
uint8_t terminate = 0;
uint16_t c[8][6];
unsigned long t;

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
  Wire.begin();
  delay(10);

  Serial.begin(230400);
//  Serial.begin(115200);
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
  pinMode(3, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(3), limit_switch_x1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(2), limit_switch_x2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(18), limit_switch_y1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), limit_switch_y2, CHANGE);

  // Slightly back off of limit switches if pressed and lift carriage
  //  startup_motors();
  //  Serial.println("11");


  ////////////////////////////////////////////////////////////////////////////////////////////////////



  byte c_addr[6] = {0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC}; // C1-C6 calibration value addresses

  //  Loop for population 2d array of calibration values
  for (int i = 0; i < 8; i++) {
    channel_select(i);
    reset_sensor();
    delay(1);
    for (int j = 0; j < 6; j++) {
      c[i][j] = read_data16(c_addr[j]); // store calibration value
    }
  }
  ////////////////////////////////////////////////////////////////////////////////////////////////////
  Serial.println("12");
}



void loop() {
  //  Serial.println("looping");
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
  char temp[32] = {};

  if (newData == true) {
    // Parse other values
    int len = strlen(receivedChars);
    //    Serial.println(len);
    //    Serial.println(receivedChars);
    for (int i = 0; i < len + 1; i++) {
      if ((receivedChars[i] != ',') && (i != len)) {
        temp[t_idx] = receivedChars[i];
        //        Serial.print("temp0 "); Serial.println(temp);
        t_idx++;
      }
      else {
        temp[t_idx] = '\0';
        //        Serial.print("temp "); Serial.println(temp[t_idx]); // Serial.print(" "); Serial.println(temp[t_id]);
        c[c_idx] = atoi(temp);
        //        Serial.println(c[c_idx]);
        c_idx++;
        t_idx = 0;
        char temp[32] = {};
      }
    }
    if (c[0] == 0) {
      Serial.println(c[0]);
      while (true);
    }
    else if (c[0] == 1) {
      Serial.println(c[0]);
      bool get_temp = false;
      if (c[1] == 1) {
        get_temp = true;
      }
      writeSensorData(get_temp);
    }
    else if (c[0] == 2) {
      Serial.println(c[0]);
      float coords[2] = {c[1] / 10.0, c[2] / 10.0};
      //      Serial.print(coords[0]); Serial.print("  "); Serial.println(coords[1]);
      moveToPos_mm(coords);
      Serial.println(c[0]);
      //      Serial.print((int) stepperX.currentPosition()); Serial.print(", "); Serial.println((int) stepperY.currentPosition());
    }
    else if (c[0] == 3) {
      Serial.println(c[0]);
      int steps[2] = {c[1], c[2]};
      moveSteps(steps, false);
      Serial.println(c[0]);
    }
    else if (c[0] == 4) {
      Serial.println(c[0]);
      if (c[1] == 0) {
        raiseZ();
      }
      else if (c[1] == 1) {
        lowerZ();
      }
      else if (c[1] == 2) {
        // do nothing for now, but can add in degree motion of z-axis when I make a function for that
      }
      Serial.println(c[0]);
    }
    else if (c[0] == 5) {
      Serial.println(c[0]);
      startup_motors();
      Serial.println(c[0]);
    }
    else if (c[0] == 6) {
      Serial.println(c[0]);
      runToLimitSwitches();
      Serial.println(c[0]);
    }
    else if (c[0] == 7) {
      Serial.println(c[0]);
      int homeOffsets[2] = {};
      getOffset(homeOffsets);
      Serial.print(homeOffsets[0]); Serial.print(", "); Serial.println(homeOffsets[1]);
    }
    else if (c[0] == 8) {
      Serial.println(c[0]);
      int steps[2] = {getStepsXY(c[1]), getStepsXY(c[2])};
      stepperX.setCurrentPosition(steps[0]);
      stepperY.setCurrentPosition(steps[1]);
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


void startup_motors() {
  int sx1 = digitalRead(3);
  int sx2 = digitalRead(2);
  int sy1 = digitalRead(18);
  int sy2 = digitalRead(19);

  int ls_steps = getStepsXY(10.0);
  int steps[2] = {0, 0};
  //  raiseZ();
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
  //  Serial.println(getStepsXY(pos[0]));
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
      while ((stepperX.distanceToGo() != 0) ||  (stepperY.distanceToGo() != 0)) {
        stepperX.run();
        stepperY.run();
      }
    }
    stepperX.run();
    stepperY.run();
  }
}

void raiseZ() {
  stepperZ.moveTo(-40);
  while (stepperZ.distanceToGo() != 0) {
    stepperZ.run();
  }
}

void lowerZ() {
  stepperZ.moveTo(40);
  while (stepperZ.distanceToGo() != 0) {
    stepperZ.run();
  }
}

// Get number of steps needed to move a certain distance along x or y axis
int getStepsXY(float distance) {
  //  float non_whole_steps = distance * stepsPerRevolutionXY / screw_lead;
  //  Serial.println(non_whole_steps);
  int steps = round(distance * stepsPerRevolutionXY / screw_lead);
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
    int val = digitalRead(3);
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
    int val = digitalRead(2);
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

///////////////////////////// SENSOR CODES ///////////////////////////////////


void writeSensorData(bool get_temp) {
  int32_t S[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  getSensorData(S, get_temp);
  for (int i = 0; i < 7; i++) {
    Serial.print(S[i]); Serial.print(", ");
  }
  Serial.println(97410);
}


void getSensorData(int32_t *s_array, bool get_temp) {
  long sensor_time = 0;
  for (int i = 0; i < 7; i++) {
    uint32_t pressure = digital_pressure_val(i);
    uint32_t temperature = digital_temperature_val(i);

    int32_t dT = temperature - (c[i][4] * pow(2, 8));
    int32_t TEMP = 2000.0 + (dT * c[i][5] / pow(2, 23));

    int64_t OFF = c[i][1] * pow(2, 16) + (c[i][3] * dT) / pow(2, 7);
    int64_t SENS = c[i][0] * pow(2, 15) + (c[i][2] * dT) / pow(2, 8);
    if (get_temp) {
      s_array[i] = TEMP;
    }
    else {
      s_array[i] = (pressure * SENS / pow(2, 21) - OFF) / pow(2, 13);
    }
  }
}

void channel_select(uint8_t i) {
  if (i > 7) return;  // exceeds max num of channels
  current_channel = i; // update active channel
  Wire.beginTransmission(mux_addr);
  Wire.write(1 << i);
  Wire.endTransmission();
}

void send_command(byte command) {
  Wire.beginTransmission(sensor_addr);
  Wire.write(command);
  Wire.endTransmission();
}

void reset_sensor() {
  send_command(0x1E);
}

void start_conv(byte osr) {
  send_command(osr);  // start conversion
  delay(4);           // wait for conversion
}

uint32_t read_data32(byte command) {
  // send: read ADC result
  send_command(command);

  // request bytes
  Wire.requestFrom(sensor_addr, 3);
  // get first byte if available
  if (Wire.available()) {
    uint32_t combined = Wire.read();

    // get remaining bytes
    while (Wire.available()) {
      combined = (combined << 8) | (Wire.read());
    }
    return combined;
  }
  uint32_t big_sad = 0;
  return big_sad;
}

uint16_t read_data16(byte command) {
  // send: read ADC result
  send_command(command);

  // request bytes
  Wire.requestFrom(sensor_addr, 2);

  // get first byte if available
  if (Wire.available()) {
    uint16_t combined = Wire.read();
    // get remaining bytes if present
    while (Wire.available()) {
      combined = (combined << 8) | (Wire.read());
    }
    return combined;
  }
  uint32_t big_sad = 0;
  return big_sad;
}

uint32_t digital_pressure_val(uint8_t channel) {
  // if measurement is not on active channel then switch
  if (channel != current_channel) {
    channel_select(channel);
  }
  // start pressure data conversion
  start_conv(posr2048);
  // get data
  uint32_t data = read_data32(adc_read);
  return data;
}

uint32_t digital_temperature_val(uint8_t channel) {
  // if measurement is not on active channel then switch
  if (channel != current_channel) {
    channel_select(channel);
  }
  // start pressure data conversion
  start_conv(tosr2048);
  // get data
  uint32_t data = read_data32(adc_read);
  return data;
}
