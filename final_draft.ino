
#include <Servo.h>

Servo myservo1;
// Servo myservo2;
int servo;

void setup() {
  Serial.begin(9600);
  myservo1.attach(3);
 //#myservo2.attach(9);
}

int i;
int ret_angle1, ret_angle2;
void loop() {
  if (Serial.available() > 0)
  {

      servo = int(Serial.read());
      servo = servo - 48;
      i = 1;
      int angle1 = 0;
      while (servo >= 0)
      {
        
        angle1 = angle1 + servo * i;
        i = i * 10;
        servo = Serial.read();
        servo = servo - 48;
      }
      ret_angle1 = angle1;
      servo =Serial.read();
      servo = servo - 48;
      int angle2 = 0;
      i = 1;
      while (servo >= 0)
      {
        
        angle2 = angle2 + servo * i;
        i = i * 10;
        servo = Serial.read();
        servo = servo - 48;     
      }
      ret_angle2 = angle2;
  
    
    Serial.print("angle1  :: ");
    Serial.println(ret_angle1);
    //Serial.print("angle2 :: ");
    //Serial.println(ret_angle2);
    myservo1.write(ret_angle1);
   //myservo2.write(ret_angle2);
  }
}
