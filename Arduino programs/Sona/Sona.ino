// sona out
int echoPin1 = 4;
int trigPin1 = 5;

//sona in
int echoPin2 = 6;
int trigPin2 = 7;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin2, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  int distance1 = pulseIn(echoPin1, HIGH);
  distance1 = distance1/58; // cm

  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  int distance2 = pulseIn(echoPin2, HIGH);
  distance2 = distance2/58; // cm

  while(Serial.available()>0){
    char r = Serial.read();
    if(r == 's'){
      String s = "(S";
      s = s + distance1 + "," + distance2 + ")";
      Serial.println(s);
      break;
    }
  }
}
