/*
  ReadAnalogVoltage

  Reads an analog input on pin 0, converts it to voltage, and prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/ReadAnalogVoltage
*/

char *suction_cups[] = { "1:", "2:", "3:", "4:" };

static const uint8_t pins[] = {1,2,3,4};
float voltages[4];


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  
  // Read out analog pins
  for (int i=0; i<4; i++)
  {
    // read the input on analog pin i:
    int sensorValue = analogRead(pins[i]);
    // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
    // voltages[i] = sensorValue * (5.0 / 1023.0);
    float voltage = -sensorValue * (1000.0 / 1023.0);

    Serial.print(suction_cups[i]);
    Serial.println(voltage);
    // check http://forum.arduino.cc/index.php?topic=243660.0 for better conversion
    delay(25);
  }  
}


