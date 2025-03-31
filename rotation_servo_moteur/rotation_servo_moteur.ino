#include <Servo.h>  // Inclure la bibliothèque Servo

Servo myServo;      // Créer un objet Servo pour contrôler le servomoteur

int pt_depart = 0;
int pt_arrive = 270;

void setup() {
  myServo.attach(3);  // Attacher le servomoteur à la broche 3
  serial.begin(9600);
}

void loop() {
  // Faire tourner le servomoteur de 0 à 270 degrés (gauche à droite)
  for (int angle = pt_depart; angle <= pt_arrive; angle++) {
    myServo.write(angle);  // Définir l'angle du servomoteur
    delay(50);             // Attendre 50 ms pour que le servomoteur atteigne la position
    serial.println(angle);
  }

  // Faire tourner le servomoteur de 270 à 0 degrés (droite à gauche)
  for (int angle = pt_arrive; angle >= pt_depart; angle--) {
    myServo.write(angle);  // Définir l'angle du servomoteur
    delay(50);             // Attendre 50 ms pour que le servomoteur atteigne la position
  }
}