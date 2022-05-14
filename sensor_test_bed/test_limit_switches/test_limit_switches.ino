
bool switch_x_1 = false;
bool switch_x_2 = false;
bool switch_y_1 = false;
bool switch_y_2 = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);

  pinMode(18, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
  pinMode(20, INPUT_PULLUP);
  pinMode(21, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(18), limit_switch_x1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(19), limit_switch_x2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(20), limit_switch_y1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(21), limit_switch_y2, CHANGE);
}

void loop() {

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
