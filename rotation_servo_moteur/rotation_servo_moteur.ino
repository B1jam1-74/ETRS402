#include <Servo.h>

Servo myServo;

int pt_depart = 0;
int pt_arrive = 270;

void setup() {
  myServo.attach(3);
  Serial.begin(9600);
}

void loop() {
  // Envoyer un marqueur de début
  Serial.println(9999);
  
  // Mouvement de gauche à droite
  for (int angle = pt_depart; angle <= pt_arrive; angle++) {
    myServo.write(angle/1.5);
    int moy = 0;
    for (int i=0; i<10 ;i++) {
      int sensorValue = analogRead(A0);
      moy += sensorValue;
    }
    moy = moy / 10;
    
    // Format : angle,valeur    
    Serial.println(moy);
    delay(15);
  }
  
  // Mouvement de droite à gauche
  for (int angle = pt_arrive; angle >= pt_depart; angle--) {
    myServo.write(angle/1.5);
    int moy = 0;
    for (int i=0; i<10 ;i++) {
      int sensorValue = analogRead(A0);
      moy += sensorValue;
    }
    moy = moy / 10;

    Serial.println(moy);
    delay(15);
  }
  
  // Envoyer un marqueur de fin
  Serial.println(-9999);
  delay(1000); // Pause avant de recommencer
}