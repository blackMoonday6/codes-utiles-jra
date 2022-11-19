int trig = 2;
int echo = 3;
int ad=4;//moteur avant droite
int ag=7;//mouteur avant gauche
int bd=5;//moteur avant droite
int bg=6;
long lecture_echo;
long cm;
int  vitesse;
int angle;
int velocity;
int positionn;
String reciveur;
String reciveur2;
int index;
void setup(){
 
pinMode(trig, OUTPUT);
digitalWrite(trig, LOW);
pinMode(ad,OUTPUT);
pinMode(ad,OUTPUT);
pinMode(echo, INPUT);
Serial.begin(9600);


}

void loop(){

 /* 
digitalWrite(trig, HIGH);
delayMicroseconds(10);
digitalWrite(trig, LOW);
lecture_echo = pulseIn(echo,HIGH);
cm = lecture_echo /58;

delay(15);

if(cm<50){
vitesse=map(cm,1,50,100,60);
  
analogWrite(ag,vitesse);
analogWrite(ad,vitesse);
delay(100);

}
if(cm>50){
  vitesse=0;
    
analogWrite(ag,vitesse);
analogWrite(ad,vitesse);
delay(100);
}


*/
analogWrite(ad,50);

analogWrite(ag,120);

analogWrite(bd,0);

analogWrite(bg,0);

}
