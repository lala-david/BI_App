int dustPin = 0;
float dustVal = 0;

int ledPower = 2;
int delayTime = 280;
int delayTime2 = 40;
float offTime = 9680;

void setup() {
  Serial.begin(9600);
  pinMode(ledPower, OUTPUT);
  pinMode(dustPin, INPUT);
}

void loop() {
  digitalWrite(ledPower, LOW);
  delayMicroseconds(delayTime);
  dustVal = analogRead(dustPin);
  delayMicroseconds(delayTime2);
  digitalWrite(ledPower, HIGH);
  delayMicroseconds(offTime);

  float dustDensity = (dustVal / 1024 - 0.0356) * 120000 * 0.035; 

  String quality = "Air Quality: ";

  if (dustDensity > 3000) {
    quality += "Very Bad";
  } else if (dustDensity > 1050) {
    quality += "Bad";
  } else if (dustDensity > 300) {
    quality += "Normal";
  } else if (dustDensity > 150) {
    quality += "Good";
  } else if (dustDensity >= 0) { 
    quality += "Very Good";
  } else {
    quality += "Measurement Error"; 
  }

  if (dustVal > 36.455) {
    Serial.print("Dust Density: ");
    Serial.print(dustDensity);
    Serial.print(" - ");
    Serial.println(quality);
  }

  delay(900000);  
}
