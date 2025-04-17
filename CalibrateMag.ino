/*

Outputs the magnetometer to the serial
*/
//#include <Arduino_LSM6DS3.h>
#include "Arduino_BMI270_BMM150.h";

#define BUFFER_SIZE 10
#define BUFFER_LEN BUFFER_SIZE*3

float magnetMagnitude = 0;
float angle = 0;

// number of initial sample calibration points
const int maxSamples = 5;

float magVec [3];
float mSmoothingBuffer [BUFFER_LEN];
int insertPos = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Mag sample rate = ");
  Serial.print(IMU.magneticFieldSampleRate());
  Serial.println(" Hz");
  Serial.println();

  for (int i = 0; i < 3; i++) {
    magVec[i] = 0;
  }

  for (int i = 0; i < BUFFER_LEN; i++) {
    mSmoothingBuffer[i] = 0;
  }

  Serial.print("Readings initialised");
}


void loop() {
  if (IMU.magneticFieldAvailable() && 1){
    float magnex, magney, magnez;

    // subtract out the effect of the earliest input to the buffer
    for (int i = 0; i < 3; i++) {
      magVec[i] -= mSmoothingBuffer[i * BUFFER_SIZE + insertPos];
    }

    IMU.readMagneticField(
      mSmoothingBuffer[0 * BUFFER_SIZE + insertPos],
      mSmoothingBuffer[1 * BUFFER_SIZE + insertPos],
      mSmoothingBuffer[2 * BUFFER_SIZE + insertPos]);
      
    // add back in the new value in the buffer
    for (int i = 0; i < 3; i++) {
      magVec[i] += mSmoothingBuffer[i * BUFFER_SIZE + insertPos];
    }

    float smoothMagMag;

    smoothMagMag   = sqrt(magVec[0]*magVec[0] + magVec[1]*magVec[1] + magVec[2]*magVec[2]) / (float) BUFFER_SIZE;

    float rawMagMag;
    rawMagMag   = sqrt(mSmoothingBuffer[0 * BUFFER_SIZE + insertPos]*mSmoothingBuffer[0 * BUFFER_SIZE + insertPos] + 
                       mSmoothingBuffer[1 * BUFFER_SIZE + insertPos]*mSmoothingBuffer[1 * BUFFER_SIZE + insertPos] + 
                       mSmoothingBuffer[2 * BUFFER_SIZE + insertPos]*mSmoothingBuffer[2 * BUFFER_SIZE + insertPos]);
    /*
    Serial.print(magVec[0] / (float) BUFFER_SIZE);
    Serial.print(",");
    Serial.print(magVec[1] / (float) BUFFER_SIZE);
    Serial.print(",");
    Serial.print(magVec[2] / (float) BUFFER_SIZE);
    Serial.println();
    */

    Serial.print(mSmoothingBuffer[0 * BUFFER_SIZE + insertPos]);
    Serial.print(",");
    Serial.print(mSmoothingBuffer[1 * BUFFER_SIZE + insertPos]);
    Serial.print(",");
    Serial.print(mSmoothingBuffer[2 * BUFFER_SIZE + insertPos]);
    Serial.println();

    insertPos++;
    insertPos %= BUFFER_SIZE;
  }
}
