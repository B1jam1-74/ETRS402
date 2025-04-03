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
  myServo.write(0);
  Serial.println(9999);
  Serial.flush();
  delay(2000);
  // Mouvement de gauche à droite
  for (float angle = pt_depart; angle <= pt_arrive; angle+= 3) {
    myServo.write(angle/1.5);
    int moy = 0;
    for (int i=0; i<20 ;i++) {
      int sensorValue = analogRead(A0);
      moy += sensorValue;
      delay(2);
    }
    moy = moy / 20;
    
    // Envoyer toutes les valeurs (même 370, 383, 385, etc.)
    Serial.println(moy);
    Serial.flush();
    delay(30);
  }
  
  // Mouvement de droite à gauche
  for (int angle = pt_arrive; angle >= pt_depart; angle--) {
    myServo.write(angle/1.5);
    delay(10);  // Augmenter le délai pour éviter les erreurs de transmission
  }
  
  // Attendre que le servo s'arrête complètement
  delay(500);
  
  // Envoyer un marqueur de fin
  Serial.println(-9999);
  Serial.flush();
  delay(1000); // Pause avant de recommencer
}