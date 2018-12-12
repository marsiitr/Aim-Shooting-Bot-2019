
 #include <Servo.h>
 
 Servo myservo1;
 Servo myservo2;


void setup() {
  Serial.begin(9600);
  myservo1.attach(9);
  myservo2.attach(11);
}

String servo;
int servo1;
int servo2;
int hash;

void loop() {
    if(Serial.available()>0)
    {
      servo=Serial.readString();
      hash=servo.indexOf("/");
      servo1=servo.substring(0,hash).toInt()+90;
      servo2=servo.substring(hash+1).toInt()+90;
      //Serial.println(servo1);
      Serial.println(servo1);
      
    }


    myservo1.write(servo2);
    //myservo2.write(servo2);
}
