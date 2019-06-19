int potpin=0;
float val=0;
String p = "P";
//int i;
void setup() {
  // put your setup code here, to run once:
  pinMode(potpin,INPUT);
  Serial.begin(9600);
}
void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0){
    char r = Serial.read();
    if(r == 'p'){
        val=analogRead(potpin);
        String s = "(" + p + val + ")";
        Serial.println(s);
        break;
    }
  }

}
