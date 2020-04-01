
#define MOISTURE_SENSOR_ZERO_PIN    (0)
#define MOISTURE_SENSOR_ONE_PIN     (1)
#define MOISTURE_SENSOR_TWO_PIN     (2)
#define MOISTURE_SENSOR_THREE_PIN   (3)
#define PUMP_ZERO_PIN               (4)
#define PUMP_ONE_PIN                (5)
#define PUMP_TWO_PIN                (6)
#define PUMP_THREE_PIN              (7)

#define MOISTURE_DIGITAL_VALUE_MAX  (614) //((1023UL / 500UL) * 300UL) 
#define MOISTURE_DIGITAL_VALUE_MIN  (256) // ((1023UL / 500UL) * 120UL) 

#define HUMIDITY_SENSOR_COUNT       (4)

#define GET_HUMIDITY_DATA           (1)
#define GET_MOTOR_STATES            (2)
#define TOGGLE_MOTOR_ZERO           (3)
#define TOGGLE_MOTOR_ONE            (4)
#define TOGGLE_MOTOR_TWO            (5)
#define TOGGLE_MOTOR_THREE          (6)
#define STOP_MOTORS                 (7)
#define INVALID_CMD                 (8)

#define HWSERIAL Serial1
#define USBSERIAL Serial

static String inputString = "";         // a string to hold incoming data
static boolean stringComplete = false;  // whether the string is complete
static bool motor_on[4] = {false, false, false, false};
const int motor_pins[4] = {PUMP_ZERO_PIN, PUMP_ONE_PIN, PUMP_TWO_PIN, PUMP_THREE_PIN};

void startMotor(int motor)
{
    int pin = motor_pins[motor];
    
    motor_on[motor] = false;
    digitalWrite(pin, LOW);
}

void stopMotors()
{
    for (int i = 0 ; i < 4; i++)
    {
        motor_on[i] = true;
        digitalWrite(motor_pins[i], HIGH);
    }
}

void setup() 
{
    pinMode(PUMP_ZERO_PIN, OUTPUT); 
    pinMode(PUMP_ONE_PIN, OUTPUT);
    pinMode(PUMP_TWO_PIN, OUTPUT);
    pinMode(PUMP_THREE_PIN, OUTPUT);     
    
    HWSERIAL.begin(9600);
    USBSERIAL.begin(9600);
    
    inputString.reserve(200);
    
    stopMotors();
}

void loop() 
{ 
    while (USBSERIAL.available()) {
      char inChar = (char)USBSERIAL.read();
      USBSERIAL.print(inChar);
    }
    
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
            else if (cmd == GET_MOTOR_STATES)
            {
                HWSERIAL.print(motor_on[0]); HWSERIAL.print(" "); HWSERIAL.print(motor_on[1]); HWSERIAL.print(" "); HWSERIAL.print(motor_on[2]); HWSERIAL.print(" "); HWSERIAL.println(motor_on[3]);
            }
            else if (cmd == TOGGLE_MOTOR_ZERO)
            {
                startMotor(0);
                HWSERIAL.println(motor_on[0]);
            }
            else if (cmd == TOGGLE_MOTOR_ONE)
            {
                startMotor(1);
                HWSERIAL.println(motor_on[1]);
            }
            else if (cmd == TOGGLE_MOTOR_TWO)
            {
                startMotor(2);
                HWSERIAL.println(motor_on[2]);
            }
            else if (cmd == TOGGLE_MOTOR_THREE)
            {
                startMotor(3);
                HWSERIAL.println(motor_on[3]);
            }
            else if (cmd == STOP_MOTORS)
            {        
                stopMotors();
                HWSERIAL.print(motor_on[0]); HWSERIAL.print(" "); HWSERIAL.print(motor_on[1]); HWSERIAL.print(" "); HWSERIAL.print(motor_on[2]); HWSERIAL.print(" "); HWSERIAL.println(motor_on[3]);
            }
        }
        
        // clear the string:
        inputString = "";
        stringComplete = false;
    }
}
