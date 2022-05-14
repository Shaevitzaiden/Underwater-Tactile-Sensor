void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  int s1 = deg2steps(1.4);
  int s2 = deg2steps(1.5);
  int s3 = deg2steps(1.6);

  int s4 = deg2steps(-1.4);
  int s5 = deg2steps(-1.5);
  int s6 = deg2steps(-1.6);

  Serial.println(s1);
  Serial.println(s2);
  Serial.println(s3);
  Serial.println(s4);
  Serial.println(s5);
  Serial.println(s6);
}

void loop() {
  // put your main code here, to run repeatedly:

}

int deg2steps(float degrees_amount) {
  int steps = round(degrees_amount);
  return steps;
}
