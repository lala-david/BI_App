#include <MQUnifiedsensor.h>

#define Board "Arduino UNO"
#define Pin A0
#define Type "MQ-135"
#define Voltage_Resolution 5
#define ADC_Bit_Resolution 10
#define RatioMQ135CleanAir 3.6

MQUnifiedsensor MQ135(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);

void setup() {
  Serial.begin(9600);
  
  MQ135.setRegressionMethod(1);
  MQ135.setA(102.2); 
  MQ135.setB(-2.473);
  MQ135.init();
  
  float calcR0 = 0;
  for(int i = 1; i<=10; i++) {
    MQ135.update();
    calcR0 += MQ135.calibrate(RatioMQ135CleanAir);
  }
  MQ135.setR0(calcR0 / 10);
}

void loop() {
  MQ135.update();
  float ppm = MQ135.readSensor();
  Serial.print("MQ-135 PPM: ");
  Serial.println(ppm);
  
  delay(1800000);
}
