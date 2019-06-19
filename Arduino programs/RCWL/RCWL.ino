#define sensorPin 2
String r1 = "R";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0){
    char r = 'r';//Serial.read();
    if(r == 'r'){
        int sensorValue = digitalRead(sensorPin);
        String s= "(" + r1 + sensorValue + ")";
        Serial.println(s);
        break;
    }
  }
}
