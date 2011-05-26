/*
 * body.cpp
 *
 *  Created on: 09/04/2011
 *      Author: shh
 */
#include "body.h"

//#define DEF_O2
#define DEF_O3
#define DEF_CO

//#define MAC_ADDRESS "111171" //Peter
#define MAC_ADDRESS "9999" //Jan
//#define MAC_ADDRESS "0123456789AB" //Steen


void setup()
{
  Utils.blinkLEDs(500); //2 blinks indicate setup
  Utils.blinkLEDs(500);

  // Setup for Serial port over USB
  USB.begin();

	// Powers RTC up, init I2C bus and read initial values
  RTC.ON();
  ACC.ON();

  // Setting time
//  RTC.setTime("09:10:20:03:17:35:00");


  // Activate Sensor Board
  SensorGas.setBoardMode(SENS_ON);
  // Configure O2 sensor

#ifdef DEF_O2
  SensorGas.configureSensor(SENS_O2, 101);
  SensorGas.setSensorMode(SENS_ON, SENS_O2);
#endif

#ifdef DEF_O3
  SensorGas.configureSensor(SENS_SOCKET2B, 1, 10);
  SensorGas.setSensorMode(SENS_ON, SENS_SOCKET2B);
#endif

#ifdef DEF_CO
  SensorGas.configureSensor(SENS_SOCKET3B, 50, 10);
  SensorGas.setSensorMode(SENS_ON, SENS_SOCKET3B);

#endif

  delay(500);
}
void loop(){

  Utils.blinkLEDs(200); //3 blinks indicate start of loop
  Utils.blinkLEDs(200);
  Utils.blinkLEDs(200);

  float value = 0;

#ifdef DEF_O2
  USB.print("MAC: ");
  USB.print(MAC_ADDRESS);
  USB.print("; TYP: O2; VAL: ");
  value = SensorGas.readValue(SENS_O2);
  USB.println(value);
#endif

#ifdef DEF_O3
  USB.print("MAC: ");
  USB.print(MAC_ADDRESS);
  USB.print("; TYP: O3; VAL: ");
  value = SensorGas.readValue(SENS_SOCKET2B);
  USB.println(value);
#endif

#ifdef DEF_CO
  USB.print("MAC: ");
  USB.print(MAC_ADDRESS);
  USB.print("; TYP: CO; VAL: ");
  value = SensorGas.readValue(SENS_SOCKET3B);
  USB.println(value);
#endif
  delay(60000);
}

