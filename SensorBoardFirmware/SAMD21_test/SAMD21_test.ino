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

const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;
int dataNumber = 0;

double T1 = 0;
double T2 = 0;

void setup() {
  // Start Wire for I2C
  Wire.begin();
  //  //  Wire.setTimeout(5000);

  // Start serial
  Serial.begin(115200);
  while (!Serial);

  ////////////////////////////////////////////////////////////////////////////////////////////////////
  // Grab stored calibration coefficients from barometers
//  Serial.println("Attempting to grab calibration coefficients from sensors");
  byte c_addr[6] = {0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC}; // C1-C6 calibration value addresses
  //
  //  Loop for population 2d array of calibration values
  for (int i = 0; i < 8; i++) {
    channel_select(i);
    reset_sensor();
    delay(1);
    for (int j = 0; j < 6; j++) {
      c[i][j] = read_data16(c_addr[j]); // store calibration value
    }
  }

//  Serial.println("Calibration coefficients acquired");
  ////////////////////////////////////////////////////////////////////////////////////////////////////

  // Collect 100 samples, print them, and then divide by time to get sampling rate
  int32_t data[8];
  T1 = millis();
  for (int i = 0; i < 10000; i++) {
    data[8] = getData();
    
  }
//  Serial.println("actually flashed2");
//  T2 = millis();
//  double dT = T2 - T1;
//  Serial.println(dT);
//  double samp = 100.0 / ((T2 - T1) / 1000.0);
//  Serial.println(samp);
}


void loop() {

}


int32_t getData() {
  uint32_t raw_pres[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  uint32_t raw_temp[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  int32_t offset_pres[8] = {0, 0, 0, 0, 0, 0, 0, 0};

  float t[8] = {0, 0, 0, 0, 0, 0, 0, 0};

  int32_t dT;
  int32_t TEMP;
  int64_t OFF;
  int64_t SENS;

  ////////////////////////////////////////////////////////
  //////////////////// TEMPURATURE ///////////////////////
  for (int i = 0; i < 7; i++) {
    // Start pressure conversions
    channel_select(i);
    start_conv(tosr1024);
    t[i] = millis();
  }

  // Prevent start of data collection till first conversion is done
  for (int i = 0; i < 8; i++) {
    // Start pressure conversions
    channel_select(i);
    while ((millis() - t[i]) < 2.5);
    raw_temp[i] = read_data32(adc_read);
  }
  /////////////////////////////////////////////////////////
  ////////////////////// PRESSURE /////////////////////////
  for (int i = 0; i < 8; i++) {
    // Start temperature conversions
    t[i] = millis();
    channel_select(i);
    start_conv(posr1024);
  }

  // Prevent start of data collection till first conversion is done
  for (int i = 0; i < 8; i++) {
    // Start pressure conversions
    channel_select(i);
    while ((millis() - t[i]) < 2.5);
    raw_pres[i] = read_data32(adc_read);
  }

  for (int i = 0; i < 8; i++) {
    dT = raw_temp[i] - (c[i][4] * pow(2, 8));
    TEMP = 2000.0 + (dT * c[i][5] / pow(2, 23));

    OFF = c[i][1] * pow(2, 16) + (c[i][3] * dT) / pow(2, 7);
    SENS = c[i][0] * pow(2, 15) + (c[i][2] * dT) / pow(2, 8);

    offset_pres[i] = (raw_pres[i] * SENS / pow(2, 21) - OFF) / pow(2, 13);
    Serial.print(offset_pres[i]); Serial.print(" ");
  }
  Serial.println(" ");
  return offset_pres[8];
}


void reset_wire() {
  uint32_t combined;
  while (Wire.available()) {
    combined = (combined << 8) | (Wire.read());
  }
}


void channel_select(uint8_t i) {
  if (i > 7) return;  // exceeds max num of channels
  current_channel = i; // update active channel
  Wire.beginTransmission(mux_addr);
  Wire.write(1 << i);
  Wire.endTransmission();
}

void channel_select_all() {
  Wire.beginTransmission(mux_addr);
  Wire.write(0x7F);
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
