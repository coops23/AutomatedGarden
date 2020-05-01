#include <Servo.h>

#define VALVE_OPEN (145)
#define VALVE_CLOSE (45)

Servo myservo;
const int servo_pin = 9;
const int mosfet_gate_pin = 10;

const int host_state_pin = 5;
const int host_enable_pin = 6;


void setup() 
{
  Serial.begin(9600);

  pinMode(host_state_pin, INPUT);
  pinMode(host_enable_pin, INPUT);
  
  pinMode(mosfet_gate_pin, OUTPUT);
  myservo.attach(servo_pin);
}

void loop() {

  int host_enable = digitalRead(host_enable_pin);
  if (host_enable == HIGH)
  {
    digitalWrite(mosfet_gate_pin, HIGH);
    int host_state = digitalRead(host_state_pin);
    if (host_state == HIGH)
    {
      myservo.write(VALVE_OPEN); 
    }
    else
    {
      myservo.write(VALVE_CLOSE);
    }  
  }
  else
  {
    digitalWrite(mosfet_gate_pin, LOW);  
  } 

  delay(15);
}


