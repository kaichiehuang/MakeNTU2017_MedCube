#include <SoftwareSerial.h>   // 引用程式庫
#define PRINT
// 定義連接藍牙模組的序列埠
SoftwareSerial BT(8, 9); // 接收腳, 傳送腳
char val;  // 儲存接收資料的變數
const int xPin = A0;
const int yPin = A1;
const int buttonPin = 5;

const int xThreshold[7] = { 147, 294, 441, 589, 736, 883, 1030 };

void setup() {
  Serial.begin(9600);   // 與電腦序列埠連線
  Serial.println("BT is ready!");
  pinMode(3, OUTPUT);
  pinMode(xPin, INPUT);
  pinMode(yPin, INPUT);
  pinMode(buttonPin, INPUT);
  digitalWrite(3, HIGH);
  // 設定藍牙模組的連線速率
  // 如果是HC-05，請改成38400
  BT.begin(115200);
}

void loop() {
  // 若收到「序列埠監控視窗」的資料，則送到藍牙模組

  int xVal = analogRead(xPin);
  int yVal = analogRead(yPin);
  bool fire = digitalRead(buttonPin);
#ifdef PRINT
  Serial.print("X: ");
  Serial.println(xVal);
  Serial.print("Y: ");
  Serial.println(yVal);
  Serial.print("Fire: ");
  Serial.println(fire);
  Serial.println("----------------");
#endif

  uint8_t sendByte = 0;

  if (fire == 1)
    sendByte = 0b10000000;

  if (xVal <= xThreshold[3]) { //0xx
    if (xVal <= xThreshold[1]) { //00x
      if (xVal >= xThreshold[0]) //001
        sendByte = sendByte | 0b00010000;
    }
    else { //01x
      sendByte = sendByte | 0b00100000;
      if (xVal >= xThreshold[2]) //011
        sendByte = sendByte | 0b00010000;
    }
  }
  else { //1xx
    sendByte = sendByte | 0b01000000;
    if (xVal <= xThreshold[5]) { //10x
      if (xVal >= xThreshold[4]) //101
        sendByte = sendByte | 0b00010000;
    }
    else { //11x
      sendByte = sendByte | 0b00100000;
      if (xVal >= xThreshold[6]) //111
        sendByte = sendByte | 0b00010000;
    }
  }

  if (yVal >= 512) sendByte = sendByte | 0b00001000;

  yVal = abs(yVal - 512);
  //sendByte = sendByte | ((yVal + 73) / 36);
  
  if (yVal <= xThreshold[3] / 2) { //0xx
    if (yVal <= xThreshold[1] / 2) { //00x
      if (yVal >= xThreshold[0] / 2) //001
        sendByte = sendByte | 0b00000001;
    }
    else { //01x
      sendByte = sendByte | 0b00000010;
      if (yVal >= xThreshold[2] / 2) //011
        sendByte = sendByte | 0b00000001;
    }
  }
  else { //1xx
    sendByte = sendByte | 0b00000100;
    if (yVal <= xThreshold[5] / 2) { //10x
      if (yVal >= xThreshold[4] / 2) //101
        sendByte = sendByte | 0b00000001;
    }
    else { //11x
      sendByte = sendByte | 0b00000010;
      if (yVal >= xThreshold[6] / 2) //111
        sendByte = sendByte | 0b00000001;
    }
  }

  BT.write(sendByte);
  Serial.println(sendByte);
  delay(50);

  // 若收到藍牙模組的資料，則送到「序列埠監控視窗」
  while (BT.available()) {
    val = BT.read();
    Serial.print(val);
  }
}
