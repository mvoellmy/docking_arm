/*
  DigitalReadSerial

  Reads a digital input on pin 2, prints the result to the Serial Monitor

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/DigitalReadSerial
*/

int count = 0;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  // print out the state of the button:
  Serial.println("Hello World");
  Serial.println(count);
  delay(1000);        // delay in between reads for stability
  count++;
}

