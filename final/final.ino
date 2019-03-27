
#include <Stepper.h>
#include <Servo.h>

#define  l_motor_g 7
#define l_motor_r 8
#define rt 2
#define rd 3
#define l_motor_g1 51
#define l_motor_r1 53

const int stepsPerRevolution = 400;
k
double kp = -1.15, kd = -0.85, ki = 0;
float error = 0, prev_error = 0, diff_error = 0, sum_error = 0;
float motor_out = 0;

Stepper myStepper(stepsPerRevolution, 5, 6);
Servo myservo;

void setup() {
  Serial.begin(9600);
  Serial1.begin(38400);
  myStepper.setSpeed(5);
  myservo.attach(9);
  myservo.write(80);
  delay(1000);
  myservo.write(0);
  delay(1000);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);

  pinMode(rd, INPUT_PULLUP);
  pinMode(rt, INPUT_PULLUP);
  pinMode(l_motor_r, OUTPUT);
  pinMode(l_motor_g, OUTPUT);
}

int angle(int a)
{
  int ang;
  if (a >= 16)
  {
    ang = a - 16;
  }
  else
  {
    ang = 0;
  }
  if (a >= 32)
    ang = ang - 32;

  return ang;
}

int state(int a)
{
  int s;
  if (a >= 32)
  {
    s = 1;
  }
  else
  {
    s = 0;
  }
  return s;
}

void rotate(int angle)
{
  int k;
  int steps = int(angle * stepsPerRevolution / 360.0);

  //steps /= 1;
  myStepper.step(steps);
}

void shoot()
{
  myservo.write(80);
  delay(1000);
  myservo.write(0);
  delay(100);
}

void follow(int x, int angle1)
{
  if (x == 1)
  {
    error = angle1;
    diff_error = error - prev_error;
    motor_out = kp * error + kd * diff_error + ki * sum_error;
    prev_error = error;
  }
  else {
    //      error=prev_error;
    //Serial.print("prev_out:  ");
    //Serial.println(error);
  }

  /*   loop_no++;

     if (loop_no == 2){
       Serial.println(error);
       Serial.println(motor_out);
       loop_no=0;
       }
  */

  if (abs(angle1) >= 2 && abs(angle1) <= 15) {
    rotate(motor_out / 3);
  }
}

void reload()
{
  int angle1, b, st;
  int rd_, rt_;
  rd_ = digitalRead(rd);
  rt_ = digitalRead(rt);
  while (rd_ != LOW)
  {
    digitalWrite(l_motor_r, LOW);
    digitalWrite(l_motor_g, HIGH);
    digitalWrite(l_motor_r1, LOW);
    digitalWrite(l_motor_g1, HIGH);
    //digitalWrite(10, HIGH);
    rd_ = digitalRead(rd);
    rt_ = digitalRead(rt);
  if(Serial1.available()>0)
  {
    b = read_values();
    st = int(b / 100);
    angle1 = b % 100 - 16;
    follow(st, angle1);
  }
    
    Serial.println("reloading");
    Serial.print("angle :");
    Serial.println(angle1);
    Serial.print("state :");
    Serial.println(st);

    Serial.print("rd  1  :");
    Serial.println(rd_);

    Serial.print("rt  1  :");
    Serial.println(rt_);
  }

  while (rt_ != LOW)
  {
    digitalWrite(l_motor_r, HIGH);
    digitalWrite(l_motor_g, LOW);
    digitalWrite(l_motor_r1, HIGH);
    digitalWrite(l_motor_g1, LOW);
    digitalWrite(10, HIGH);
    rd_ = digitalRead(rd);
    rt_ = digitalRead(rt);

    if (Serial1.available()>0)
    {
      b = read_values();
      st = int(b / 100);
      angle1 = b % 100 - 16;
      follow(st, angle1);
    }
    

    Serial.print("rd  :");
    Serial.println(rd_);
    Serial.print("rt  :");
    Serial.println(rt_);

  }

  digitalWrite(l_motor_r, LOW);
  digitalWrite(l_motor_g, LOW);
}

int read_values()
{
  int a, ang, st;
  
    a = Serial1.read();
    ang = angle(a);
    st = state(a);
    Serial.print("a :");
    Serial.println(a);
  
  return st * 100 + ang + 16;
}

int sht_cnt = 0;

void loop() {
  
  int st;
  int angle1, b;
  
  if (Serial1.available() > 0)
  { 
    b = read_values();
    st = int(b / 100);
    angle1 = b % 100 - 16;
    
    Serial.print("angle :");
  Serial.println(angle1);
  Serial.print("state :");
  Serial.println(st);
  
  follow(st, angle1);
  if (st == 1 && abs(angle1) <= 2)
    sht_cnt++;
  else
    sht_cnt = 0;

  /*Serial.print("counter :");uuu
    Serial.println(sht_cnt);*/
  if (sht_cnt > 2)
  {
    Serial.println("shooting and reloading");
    shoot();
    reload();
    sht_cnt=0;
  }

  }

}
