#include <SPI.h>
#include <Wire.h>
#include <SparkFun_MicroPressure.h>
#include <SparkFun_RV1805.h>
#include <Servo.h>
#include <RH_RF95.h>
byte profcount = 0;
RV1805 rtc;
Servo servo;
SparkFun_MicroPressure mpr;
#define DEBUG true
//I2C Library
char datap[1500];
uint8_t dataps[1500];
char charPres[4];
char datat[1500];
uint8_t datats[1500];
char charTemp[4];

//Radio Head Library:
RH_RF95 rf95(12, 6);
byte canWeLeave = 1;
byte buf[RH_RF95_MAX_MESSAGE_LEN];
byte len = sizeof(buf);

int LED = 13;  // Status LED is on pin 13
char go[] = "go";
int packetCounter = 0;
float atmosphere = 14.7;
float pTollerance = 0.2;  // Tollerance for the top pressure trigger
float topPressure;
int topButton = 3;     // pin for the top tigger
int bottomButton = 4;  // pin fo  r the bottom trigger
int servoPin = 9;      // Pin for the Servo
int motorOut = 1370;   // maximun microseconds the motor can go
int pressure;
int looop = 0;
int lenth = 4;
int time;
int c = 0;
int cc = 0;

// The broadcast frequency is set to 921.2, but the SADM21 ProRf operates
// anywhere in the range of 902-928MHz in the Americas.
float frequency = 921.2;


void connectionCheck() {
  uint8_t toSend[] = "198";
  int count = 1;
  while (true) {
    //Send a message to the other radio
    rf95.send(toSend, sizeof(toSend));
    rf95.waitPacketSent();

    // Now wait for a reply
    byte buf[RH_RF95_MAX_MESSAGE_LEN];
    byte len = sizeof(buf);

    if (rf95.waitAvailableTimeout(500)) {
      // Should be a reply message for us now
      if (rf95.recv(buf, &len)) {
        if (DEBUG) SerialUSB.print("Got reply: ");
        if (DEBUG) SerialUSB.println((char*)buf);
        break;
      }

      delay(500);
    }
  }
}



void waitForGo() {
  // exits the funtion when the float recives the "Go"
  while (true) {
    byte buf[RH_RF95_MAX_MESSAGE_LEN];
    buf[0] = (char)"0"[0];
    buf[1] = (char)"0"[0];
    SerialUSB.println((char*)buf);
    byte len = sizeof(buf);
    if (rf95.waitAvailableTimeout(500)) {
      // Should be a reply message for us now
      if (rf95.recv(buf, &len)) {
        for (int i = 0; i < 5; i++) {
          if (DEBUG) SerialUSB.println((char*)buf);
        }

        if (((char*)buf)[0] == (char)"g"[0]) {
          break;
        }
      }
    }
  }
}



void gatherData() {
  pressure = abs((mpr.readPressure() - atmosphere)) * 1000;  // remove -10 when in water

  itoa(pressure, charPres, 10);
  SerialUSB.println(pressure);
  if (pressure < 1000) {
    if (pressure < 100) {
      if (pressure < 10) {
        datap[c * 5] = (char)"0"[0];
        datap[c * 5 + 1] = (char)"0"[0];
        datap[c * 5 + 2] = (char)"0"[0];
        for (int i = 0; i <= 3; i++) {
          datap[c * 5 + i] = (char)"0"[0];
          datap[c * 5 + i + 3] = (charPres[i]);
        }
      } else {
        datap[c * 5] = (char)"0"[0];
        datap[c * 5 + 1] = (char)"0"[0];
        for (int i = 0; i <= 3; i++) {

          datap[c * 5 + i + 2] = (charPres[i]);
        }
      }
    } else {
      datap[c * 5] = (char)"0"[0];
      for (int i = 0; i <= 3; i++) {

        datap[c * 5 + i + 1] = (charPres[i]);
      }
    }
  } else {
    for (int i = 0; i <= 3; i++) {
      datap[c * 5 + i] = (charPres[i]);
    }
  }

  datap[(c * 5) + 4] = (char)","[0];

  for (int i = 0; i <= 1500; i++) {
    SerialUSB.print(datap[i]);
  }
  SerialUSB.println();
  rtc.updateTime();
  int time = rtc.getSeconds() + (rtc.getMinutes() * 60);
  itoa(time, charTemp, 10);
  SerialUSB.println(charTemp);
  lenth = (strlen(charTemp));

  for (int i = 0; i <= lenth; i++) {
    datat[c * (lenth + 1) + i] = charTemp[i];
  }

  datat[(c * (lenth + 1)) + lenth] = (char)","[0];

  for (int i = 0; i <= 1500; i++) {
    SerialUSB.print(datat[i]);
  }
  SerialUSB.println();

  c++;
}



void sendData() {
  // Converting arrays to Unint-8
  for (int i = 0; i < sizeof(datap) - 1; i++) {
    dataps[i] = datap[i];
  }
  for (int i = 0; i < sizeof(datat) - 1; i++) {
    datats[i] = datat[i];
  }

  // Send the data
  for (int i = 0; i < 3 - 1; i++) {
    SerialUSB.println(datap[0]);
    rf95.send(dataps, sizeof(dataps));
    rf95.waitPacketSent();
    delay(500);

    SerialUSB.println("Sending packets");
    SerialUSB.println(datat[0]);

    rf95.send(datats, sizeof(datats));
    rf95.waitPacketSent();
    delay(500);
  }
}



void clearArrays() {
  // Cears the arrays for new data
  cc = 0;
  c = 0;

  for (int i = 0; i <= 1499; i++) {
    datat[i] = (char)"0"[0];
  }
  for (int i = 0; i <= 3; i++) {
    datap[c * 5 + i] = (char)"xadfh"[profcount % 5];
  }

  datap[(c * 5) + 4] = (char)","[0];
  int time = rtc.getSeconds() + (rtc.getMinutes() * 60);
  itoa(time, charTemp, 10);
  lenth = (strlen(charTemp));
  datat[0] = (char)"ycegi"[profcount % 5];
  datat[lenth] = (char)","[0];
  profcount++;
  c++;
}



void setup() {
  SerialUSB.begin(9600);
  Wire.begin();
  servo.attach(servoPin);
  pinMode(bottomButton, INPUT);
  pinMode(topButton, INPUT);

  // "Prime" the bouyancy engine
  servo.writeMicroseconds(motorOut);
  delay(3000);
  servo.writeMicroseconds(1000);
  //delay(2000);
  //servo.writeMicroseconds(1182);

  // Failcheck the RTC
  if (rtc.begin() == false) {
    SerialUSB.println("Something went wrong, check wiring");
  }
  if (rtc.setTime(0, 0, 0, 0, 0, 3, 2078, 21) == false) {
    SerialUSB.println("Something went wrong setting the time");
  }

  // Failcheck the Pressure Sensor
  if (!mpr.begin()) {
    SerialUSB.println("Cannot connect to MicroPressure sensor.");
    while (1)
      ;
  }

  // Failcheck the radio
  if (rf95.init() == false) {
    SerialUSB.println("Radio failed to initialize");
    while (1)
      ;
  }

  // Setting up the radio
  rf95.setFrequency(frequency);
  rf95.setTxPower(14, false);
  connectionCheck();
}



void loop() {
  SerialUSB.println("can I go yet?????");
  waitForGo();
  SerialUSB.println("got go :)");
  topPressure = mpr.readPressure();
  clearArrays();

  // Decending Loop
  while (true) {
    servo.writeMicroseconds(motorOut);
    SerialUSB.println("Decending");

    gatherData();
    delay(5000);

    if (digitalRead(bottomButton) == HIGH) {
      break;
    }
  }

  // Acending Loop
  while (true) {
    servo.writeMicroseconds(1000);
    SerialUSB.println("Acending");

    gatherData();
    delay(5000);

    if (((mpr.readPressure() <= topPressure + pTollerance) && (mpr.readPressure() >= topPressure - pTollerance)) || (digitalRead(topButton) == HIGH)) {
      sendData();
      break;
    }
  }
}
