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
#define sensor1 25
#define sensor2 26
BluetoothSerial SerialBT;
//here we setup the two bno sensors to use the different lines. Notice that they have the same address
//which is okay
//since they communicate on different lines.
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28, &I2Cone);
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &I2Ctwo);

void setup() {
  SerialBT.begin("Icebear");
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


  //SerialBT.print("\nKnee Flexion Angle:\t\t    Hip Flexion Angle:\n");
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



//KNEE
  if (gyro1 == 3 && euler1.x() != 0 && euler1.y() != 0 && euler1.z() != 0) {
      SerialBT.print(euler1.z()-90);
      SerialBT.print(",");
  
  }
  //HIP
  if (gyro2 == 3 && euler2.x() != 0 && euler2.y() != 0 && euler2.z() != 0) {
    //SerialBT.print("θ2: ");
    SerialBT.print(abs(euler2.z()-90));
    SerialBT.print(",");
  }

  float force1_reading = abs(analogRead(sensor1));
  //SerialBT.print("Toe Sensor: ");
  SerialBT.print(force1_reading);
  SerialBT.print(",");

  float force2_reading = abs(analogRead(sensor2));
  SerialBT.println(force2_reading);
  delay(BNO055_SAMPLERATE_DELAY_MS);
}