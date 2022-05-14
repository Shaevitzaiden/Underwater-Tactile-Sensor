#include <AccelStepper.h>

/*  Project: Code for controlling XY positioning table for tactile sensor testing
    Name: Aiden Shaevitz
    Date: 3/31/2022
*/

const int switch_pin_x = 2;
const int switch_pin_y = 3;
const int switch_pin_z_top = 4;
const int switch_pin_z_bot = 5;

bool switch_state_x = false;
bool switch_state_y = false;
bool switch_state_z_top = false;
bool switch_state_z_bot = false;

const int screw_lead = 8; // mm/rotation
const int stepsPerRevolutionXY = 1600;  // change this to fit the number of steps per revolution
const int stepsPerRevolutionZ = 200;
float current_pos[] = {1000000000., 1000000000.}; // Set very high so that when homing it will always reach the true zero position

// Initialize the stepper library on pins 8 through 12:
AccelStepper stepperX(AccelStepper::DRIVER, 8, 9);
AccelStepper stepperY(AccelStepper::DRIVER, 7, 10);
AccelStepper stepperZ(AccelStepper::DRIVER, 12, 11);


void setup() {
  // initialize the serial port:
  Serial.begin(9600);
  while (!Serial);

  // set stepper parameters
  stepperX.setMaxSpeed(200.0);
  stepperX.setAcceleration(100.0);

  stepperY.setMaxSpeed(200.0);
  stepperY.setAcceleration(100.0);

  stepperZ.setMaxSpeed(200.0);
  stepperZ.setAcceleration(100.0);

  // Initialize pins for x and y limit switches and attach interrupts
  pinMode(switch_pin_x, INPUT_PULLUP);
  pinMode(switch_pin_y, INPUT_PULLUP);
  pinMode(switch_pin_z_top, INPUT_PULLUP);
  pinMode(switch_pin_z_bot, INPUT_PULLUP);
//  attachInterrupt(digitalPinToInterrupt(switch_pin_x), xLim, CHANGE); // will be responsible for both x limit switches
//  attachInterrupt(digitalPinToInterrupt(switch_pin_y), yLim, CHANGE); // will be responsible for both y limit switches
//  attachInterrupt(digitalPinToInterrupt(switch_pin_z_top), zLimTop, CHANGE); // will be responsible for top limit switch along z axis
//  attachInterrupt(digitalPinToInterrupt(switch_pin_z_bot), zLimBot, CHANGE); // will be responsible for bottom limit switch along z axis
  delay(5);

  homingSequence();
}


void loop() {

}


void homingSequence() {
  // Move x-axis to limit switch
  float home_pos[2] = {0., 0.}; 
  bool reached_home = false;
  
  //  * save location as 0
  //  * back off amount x
  //  * move back to limit switch and determine difference in limit switch triggering point
  //  * repeat for n times and average 0 locations to get a "true" zero

  // Repeat above steps for y-axis

  // Repeat above steps for z-axis if necessary, significantly less precision is needed
}


// Positions in mm
void moveToPos(float next_pos[2]) {
  float dX = next_pos[0] - current_pos[0];
  float dY = next_pos[1] - current_pos[1];

  int steps_x = getStepsXY(dX);
  int steps_y = getStepsXY(dY);

  stepperX.move(steps_x);
  stepperY.move(steps_y);

  bool move_status_x = true;
  bool move_status_y = true;

  while (move_status_x) && (move_status_y) {
    // check if limit switch tripped
    if (switch_state_x) || (switch_state_y) {
      earlyTermination();
    }
    switch_state_x = stepperX.run();
    switch_state_x = stepperY.run();
  }
}

void raiseProbe(){
  // may just want to use limit switches to determine stopping condition for the z-stepper
  stepperZ.move(steps_z);
  bool move_status_z = true;
  while (move_status_z){
    move_status_z = stepperZ.run()
  }
}

void lowerProbe(){
  // may just want to use limit switches to determine stopping condition for the z-stepper
  stepperZ.move(steps_z);
  bool move_status_z = true;
  while (move_status_z){
    move_status_z = stepperZ.run()
  }
  

// Triggers if limit switches trigger during a normal motion operation
void earlyTermination() {
  stepperX.stop();
  stepperY.stop();
  while (true) {
    stepperX.run();
    stepperY.run();
    Serial.println('Early termination triggered, please reset');
  }
}


// Get number of steps needed to move a certain distance along x or y axis
int getStepsXY(float distance) {
  int steps = round(distance / (screw_lead / stepsPerRevolutionXY))
              return steps
}

// Get number of steps needed to move probe a certain distance along z-axis
int getStepsZ(float distance) {
  // Will need to change this function once I design the cam for lifting the probe/weights carriage
  int steps = round(distance / (10000000.00000 / stepsPerRevZ))
              return steps
}


//----------------------------- LIMIT SWITCH INTERRUPT FUNCTIONS --------------------------
void xLim() {
  if (!switch_x_state) {
    switch_state_x = true;
  }
  else if (switch_x_state) {
    switch_state_x = false;
  }
}

void yLim() {
  if (!switch_y_state) {
    switch_state_y = true;
  }
  else if (switch_y_state) {
    switch_state_y = false;
  }
}

void zLimTop(){
  if (!switch_state_z_top) {
    switch_state_y = true;
  }
  else if (switch_state_z_top) {
    switch_state_y = false;
  }
}

void zLimBot(){
  if (!switch_state_z_bot) {
    switch_state_y = true;
  }
  else if (switch_state_z_bot) {
    switch_state_y = false;
  }
}
//-----------------------------------------------------------------------------------------
