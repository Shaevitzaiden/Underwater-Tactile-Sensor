/**
  name: Aiden Shaevitz
  date: January 2022
  description: code for reading custom sensor board with 8 MS5837-30 temperature-pressure
             sensors via an 8 channel i2c multiplexer
*/

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

const byte interrupt_pin = 2;
uint8_t current_channel = 0;
uint8_t terminate = 0;
uint16_t c[8][6];
unsigned long t;

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;
int dataNumber = 0;


void setup() {
  Wire.begin();
  delay(10);

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
  Serial.begin(115200);
  clearInputBuffer();
  Serial.println("1");
}

void clearInputBuffer() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

void loop() {
  recvWithStartEndMarker();
  parseCommands();
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
      writeSensorData();
    }
    else if (c[0] == 2) {
      Serial.println(c[0]);
    }
    newData = false;
  }
}

void controlLoop() {
  boolean inControl = true;
  while (inControl) {
  }
}

void writeSensorData() {
  int32_t P[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  getSensorData(P);
  for (int i = 0; i < 7; i++) {
    Serial.print(P[i]); Serial.print(", ");
  }
  Serial.println(P[7]);
}

void getSensorData(int32_t *p_array) {
  for (int i = 0; i < 8; i++) {
    uint32_t pressure = digital_pressure_val(i);
    uint32_t temperature = digital_temperature_val(i);

    int32_t dT = temperature - (c[i][4] * pow(2, 8));
    int32_t TEMP = 2000.0 + (dT * c[i][5] / pow(2, 23));

    int64_t OFF = c[i][1] * pow(2, 16) + (c[i][3] * dT) / pow(2, 7);
    int64_t SENS = c[i][0] * pow(2, 15) + (c[i][2] * dT) / pow(2, 8);
    p_array[i] = (pressure * SENS / pow(2, 21) - OFF) / pow(2, 13);
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
