#include <Wire.h>

//each data of acc is 2 bytes
const int MPU = 0x68; // MPU-6050 I2C address
const int nValCnt = 3; // number of data to read

const int nCalibTimes = 1000; //校准时读数的次数
int calibData[nValCnt]; //校准数据



void setup() {
  Serial.begin(9600);
  Wire.begin();
  WriteMPUReg(0x6B, 0);
}

void loop() {
  int readouts[nValCnt];
  ReadAcc(readouts);

  float realVals[nValCnt];
  Rectify(readouts, realVals);
  while(Serial.available()>0){
    char first = Serial.read();
    //door: d
    //window: w
    if(first == 'w'){
      float x = realVals[0];
      float y = realVals[1];
      float z = realVals[2];
      String s = "(W";
      s = s + x + "," + y + "," + z + ")";
      Serial.println(s);
    }
  }
}


void WriteMPUReg(int nReg, unsigned char nVal) {
  Wire.beginTransmission(MPU);
  Wire.write(nReg);
  Wire.write(nVal);
  Wire.endTransmission(true);
}
void ReadAcc(int *pVals) {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.requestFrom(MPU, nValCnt * 2, true);
  Wire.endTransmission(true);
  for (long i = 0; i < nValCnt; ++i) {
    pVals[i] = Wire.read() << 8 | Wire.read();
  }
}
//对大量读数进行统计，校准平均偏移量
void Calibration()
{
  float valSums[7] = {0.0f, 0.0f, 0.0f};
  //先求和
  for (int i = 0; i < nCalibTimes; ++i) {
    int mpuVals[nValCnt];
    ReadAcc(mpuVals);
    for (int j = 0; j < nValCnt; ++j) {
      valSums[j] += mpuVals[j];
    }
  }
  //再求平均
  for (int i = 0; i < nValCnt; ++i) {
    calibData[i] = int(valSums[i] / nCalibTimes);
  }
  calibData[2] += 16384; //设芯片Z轴竖直向下，设定静态工作点。
}

//对读数进行纠正，消除偏移，并转换为物理量
void Rectify(int *pReadout, float *pRealVals) {
  for (int i = 0; i < 3; ++i) {
    pRealVals[i] = (float)(pReadout[i] - calibData[i]) / 16384.0f;
  }
}
