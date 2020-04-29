#include <Servo.h>

#define MOISTURE_SENSOR_ZERO_PIN    (0)
#define MOISTURE_SENSOR_ONE_PIN     (1)
#define MOISTURE_SENSOR_TWO_PIN     (2)
#define MOISTURE_SENSOR_THREE_PIN   (3)

#define SERVO_PIN                   (6)
#define EN_PIN                      (7)

#define VALVE_OPEN_VALUE            (145)
#define VALVE_CLOSE_VALUE           (45)

#define HUMIDITY_SENSOR_COUNT       (4)

#define GET_HUMIDITY_DATA           (1)
#define VALVE_OPEN                  (2)
#define VALVE_CLOSE                 (3)
#define EN_HIGH                     (4)
#define EN_LOW                      (5)
#define INVALID_CMD                 (6)

#define HWSERIAL Serial1
//#define USBSERIAL Serial1

Servo valve_servo;

static String inputString = "";         // a string to hold incoming data
static boolean stringComplete = false;  // whether the string is complete

void setup() 
{
    pinMode(EN_PIN, OUTPUT); 
    valve_servo.attach(SERVO_PIN);  
    
    HWSERIAL.begin(9600);
    //USBSERIAL.begin(9600);
    
    inputString.reserve(200);
    
    digitalWrite(EN_PIN, LOW);
    valve_servo.write(VALVE_CLOSE_VALUE);
}

void loop() 
{ 
    /*while (USBSERIAL.available()) {
      char inChar = (char)USBSERIAL.read();
      USBSERIAL.print(inChar);
    }*/
    
    while (HWSERIAL.available()) {
      // get the new byte:
      char inChar = (char)HWSERIAL.read();
      // add it to the inputString:
      inputString += inChar;
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '\n') {
        stringComplete = true;
      }
    }
  
    if (stringComplete) 
    {
        char msg[32];
        int cmd = 0;
        
        inputString.toCharArray(msg, 32);
        cmd = atoi(msg);

        if (cmd <= 0)
        {
            HWSERIAL.println("Error");
        }
        else if (cmd >= INVALID_CMD)
        {
            HWSERIAL.println("Error");
        }
        else
        {
            if (cmd == GET_HUMIDITY_DATA)
            {
                int humidity[HUMIDITY_SENSOR_COUNT];

                humidity[0] = analogRead(MOISTURE_SENSOR_ZERO_PIN);
                humidity[1] = analogRead(MOISTURE_SENSOR_ONE_PIN);
                humidity[2] = analogRead(MOISTURE_SENSOR_TWO_PIN);
                humidity[3] = analogRead(MOISTURE_SENSOR_THREE_PIN);

                HWSERIAL.print(humidity[0]); HWSERIAL.print(" "); HWSERIAL.print(humidity[1]); HWSERIAL.print(" "); HWSERIAL.print(humidity[2]); HWSERIAL.print(" "); HWSERIAL.println(humidity[3]);
            }
            else if (cmd == VALVE_OPEN)
            {
                valve_servo.write(VALVE_OPEN_VALUE);
                HWSERIAL.println("opening");
            }
            else if (cmd == VALVE_CLOSE)
            {
                valve_servo.write(VALVE_CLOSE_VALUE);
                HWSERIAL.println("closing");
            }
            else if (cmd == EN_HIGH)
            {
                digitalWrite(EN_PIN, HIGH);
                HWSERIAL.println("Enabled");
            }
            else if (cmd == EN_LOW)
            {
                digitalWrite(EN_PIN, LOW);
                HWSERIAL.println("Disabled");
            }
        }
        
        // clear the string:
        inputString = "";
        stringComplete = false;
    }
}
