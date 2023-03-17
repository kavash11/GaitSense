#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "BluetoothSerial.h"
//For one I2C line in Parm’s tutorials we have -> data is blue and pin 21, clock is yellow and pin 22
#define SDA_1 21
#define SCL_1 22
//here we define the pins for the other I2C line that you wired in part 1 of the tutorial
#define SDA_2 19
#define SCL_2 23
TwoWire I2Cone = TwoWire(0);
TwoWire I2Ctwo = TwoWire(1);
#define BNO055_SAMPLERATE_DELAY_MS (100)
#define sensor1 26

BluetoothSerial SerialBT
#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

//pins:
const int HX711_dout = 5; //mcu > HX711 dout pin
const int HX711_sck = 18; //mcu > HX711 sck pin

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

const int calVal_eepromAdress = 0;
unsigned long t = 0;
//here we setup the two bno sensors to use the different lines. Notice that they have the same address
//which is okay
//since they communicate on different lines.
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28, &I2Cone);
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &I2Ctwo);
void setup() {
  SerialBT.begin("ESP32-Bluetooth"));
  Serial.begin(115200);
  SerialBT.println(F("Two BNO test"));
  //have I2C communication begin and tell I2Cone and I2Ctwo which lines are being used.
  I2Cone.begin(SDA_1, SCL_1, 100000);
  I2Ctwo.begin(SDA_2, SCL_2, 100000);
  //check if you wired it correctly. If not you will constantly print what is below
  bool status1 = bno1.begin();
  if (!status1) {
    SerialBT.println("Could not find a valid Bno_1 sensor, check wiring!");
    while (1)
      ;
  }
  bool status2 = bno2.begin();
  if (!status2) {
    SerialBT.println("Could not find a valid Bno_2 sensor, check wiring!");
    while (1)
      ;
  }
  SerialBT.println();
    LoadCell.begin();
  //LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    SerialBT.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(1.0); // user set calibration value (float), initial value 1.0 may be used for this sketch
    SerialBT.println("Startup is complete");
  }
  while (!LoadCell.update());
  calibrate(); //start calibration procedure
}
//Note that below you dont have to think about the 2 separate lines anymore. You just use bno1 when
//you want to use the first bno and bno2 when you want to use the other
void loop() {

  imu::Vector<3> euler1 = bno1.getVector(Adafruit_BNO055::VECTOR_EULER);  //obtaining euler values of sensor
  uint8_t system1, gyro1, accel1, mag1 = 0;                               //initializing variables for the calibration parameters
  uint8_t system2, gyro2, accel2, mag2 = 0;
  bno1.getCalibration(&system1, &gyro1, &accel1, &mag1);

 
  imu::Vector<3> euler2 = bno2.getVector(Adafruit_BNO055::VECTOR_EULER);  //obtaining euler values of sensor

  bno2.getCalibration(&system2, &gyro2, &accel2, &mag2);


  SerialBT.print("\nKnee Flexion Angle:\t\t    Hip Flexion Angle:\n");
  // Serial.print("Sys1=");  //displaying the calibration values for first sensor (int values, range from 0-3)
  // Serial.print(system1, DEC);
  // Serial.print(", Gyro1=");
  // Serial.print(gyro1, DEC);
  // Serial.print(", Accel1=");
  // Serial.print(accel1, DEC);
  // Serial.print(", Mag1=");
  // Serial.print(mag1, DEC);
  // Serial.print("\t ");
  // Serial.print("Sys2=");  //displaying the calibration values for second sensor (int values, range from 0-3)
  // Serial.print(system2, DEC);
  // Serial.print(", Gyro2=");
  // Serial.print(gyro2, DEC);
  // Serial.print(", Accel2=");
  // Serial.print(accel2, DEC);
  // Serial.print(", Mag2=");
  // Serial.print(mag2, DEC);
  // Serial.print("\t\t\t");
  static boolean newDataReady = 0;
  const int serialPrintInterval = 0; //increase value to slow down serial print activity

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {
    if (millis() > t + serialPrintInterval) {
      float i = LoadCell.getData();
      SerialBT.print("Load_cell output val: ");
      SerialBT.println(i);
      newDataReady = 0;
      t = millis();
    }
  }

  // receive command from serial terminal
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') LoadCell.tareNoDelay(); //tare
    else if (inByte == 'r') calibrate(); //calibrate
    else if (inByte == 'c') changeSavedCalFactor(); //edit calibration value manually
  }

  // check if last tare operation is complete
  if (LoadCell.getTareStatus() == true) {
    SerialBT.println("Tare complete");
  }
//KNEE
  if (gyro1 == 3 && euler1.x() != 0 && euler1.y() != 0 && euler1.z() != 0) {
    if (euler1.z() >= 0) {
      SerialBT.print("   θ1: ");
      SerialBT.print(euler1.z() - 90);
      SerialBT.print("\t\t\t\t ");
    } 
    else {
      SerialBT.print("   θ1: ");
      SerialBT.print(euler1.z() + 270);
      SerialBT.print("\t\t\t\t ");
    }
  }
  //HIP
  if (gyro2 == 3 && euler2.x() != 0 && euler2.y() != 0 && euler2.z() != 0) {
    SerialBT.print("θ2: ");
    SerialBT.print(euler2.z() + 90);
    SerialBT.println("\n");
  }

  float force1_reading = abs(analogRead(sensor1));
  SerialBT.print("Toe Sensor: ");
  SerialBT.println(force1_reading);
  delay(BNO055_SAMPLERATE_DELAY_MS);
}

void calibrate() {
  SerialBT.println("***");
  SerialBT.println("Start calibration:");
  SerialBT.println("Place the load cell an a level stable surface.");
  SerialBT.println("Remove any load applied to the load cell.");
  SerialBT.println("Send 't' from serial monitor to set the tare offset.");

  boolean _resume = false;
  while (_resume == false) {
    LoadCell.update();
    if (Serial.available() > 0) {
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell.tareNoDelay();
      }
    }
    if (LoadCell.getTareStatus() == true) {
      SerialBT.println("Tare complete");
      _resume = true;
    }
  }

  SerialBT.println("Now, place your known mass on the loadcell.");
  SerialBT.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

  float known_mass = 0;
  _resume = false;
  while (_resume == false) {
    LoadCell.update();
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        SerialBT.print("Known mass is: ");
        SerialBT.println(known_mass);
        _resume = true;
      }
    }
  }

  LoadCell.refreshDataSet(); //refresh the dataset to be sure that the known mass is measured correct
  float newCalibrationValue = LoadCell.getNewCalibration(known_mass); //get the new calibration value

  SerialBT.print("New calibration value has been set to: ");
  SerialBT.print(newCalibrationValue);
  SerialBT.println(", use this as calibration value (calFactor) in your project sketch.");
  SerialBT.print("Save this value to EEPROM adress ");
  SerialBT.print(calVal_eepromAdress);
  SerialBT.println("? y/n");

  _resume = false;
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        SerialBT.print("Value ");
        SerialBT.print(newCalibrationValue);
        SerialBT.print(" saved to EEPROM address: ");
        SerialBT.println(calVal_eepromAdress);
        _resume = true;

      }
      else if (inByte == 'n') {
        SerialBT.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }

  SerialBT.println("End calibration");
  SerialBT.println("***");
  SerialBT.println("To re-calibrate, send 'r' from serial monitor.");
  SerialBT.println("For manual edit of the calibration value, send 'c' from serial monitor.");
  SerialBT.println("***");
}

void changeSavedCalFactor() {
  float oldCalibrationValue = LoadCell.getCalFactor();
  boolean _resume = false;
  SerialBT.println("***");
  SerialBT.print("Current value is: ");
  SerialBT.println(oldCalibrationValue);
  SerialBT.println("Now, send the new value from serial monitor, i.e. 696.0");
  float newCalibrationValue;
  while (_resume == false) {
    if (Serial.available() > 0) {
      newCalibrationValue = Serial.parseFloat();
      if (newCalibrationValue != 0) {
        SerialBT.print("New calibration value is: ");
        SerialBT.println(newCalibrationValue);
        LoadCell.setCalFactor(newCalibrationValue);
        _resume = true;
      }
    }
  }
  _resume = false;
  SerialBT.print("Save this value to EEPROM adress ");
  SerialBT.print(calVal_eepromAdress);
  SerialBT.println("? y/n");
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        SerialBT.print("Value ");
        SerialBT.print(newCalibrationValue);
        SerialBT.print(" saved to EEPROM address: ");
        SerialBT.println(calVal_eepromAdress);
        _resume = true;
      }
      else if (inByte == 'n') {
        SerialBT.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }
  SerialBT.println("End change calibration value");
  SerialBT.println("***");
}