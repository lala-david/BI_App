#include <MQUnifiedsensor.h>
#include "MQ7.h"

#define MQ2Pin A1
#define MQ2Type "MQ-2"
#define MQ2VoltageResolution 3.5
#define MQ2ADCBits 10
#define MQ2RatioCleanAir 9.83

#define MQ7Pin A0
#define MQ7Voltage 5.0

MQUnifiedsensor MQ2("Arduino UNO", MQ2VoltageResolution, MQ2ADCBits, MQ2Pin, MQ2Type);
MQ7 mq7(MQ7Pin, MQ7Voltage);

void setup() {
  Serial.begin(115200);
  
  MQ2.setRegressionMethod(1);
  MQ2.setA(574.25);
  MQ2.setB(-2.222);
  MQ2.init();
  
  float calcR0 = 0;
  for(int i = 1; i<=10; i++) {
    MQ2.update();
    calcR0 += MQ2.calibrate(MQ2RatioCleanAir);
  }
  MQ2.setR0(calcR0 / 10);
}

void loop() {
  MQ2.update();
  float mq2ppm = MQ2.readSensor();
  Serial.print("MQ-2 LPG PPM: ");
  Serial.println(mq2ppm);
  
  float mq7ppm = mq7.getPPM();
  Serial.print("MQ-7 CO PPM: ");
  Serial.println(mq7ppm);
  
  delay(1800000);
}