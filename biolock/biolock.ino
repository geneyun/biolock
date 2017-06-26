/* This code was written by Yonatan Schachter, using the FPS_GT511C3.h library written by Josh Hawley. 2017 */

#include "FPS_GT511C3.h"
#include "SoftwareSerial.h"

//this sets up the scanner pins
FPS_GT511C3 fps(4, 5);
int LED = 7;

//this is a PIN code unique to each scanner. it is used to scramble the message
int PIN[32] = {165, 40, 143, 130, 14, 47, 181, 117, 254, 92, 158, 35, 242, 36, 69, 131, 62, 54, 139, 69, 253, 111, 200, 27, 89, 133, 128, 74, 5, 192, 208, 178};

void setup() {

  //initialization of the serial connection, the LED and the fps
  Serial.begin(9600);
  pinMode(LED,OUTPUT);
  fps.Open();

}

void loop() {

  //this checks if there is information arriving from the computer
  if(Serial.available()>0){

    //this reads whatever the computer sent and associates it to a command
    char command = Serial.read();
    switch(command){

      //turns green LED on
      case 'x':
        digitalWrite(LED,HIGH);
      break;

      //turns green LED off
      case 'y':
        digitalWrite(LED,LOW);
      break;

      //echo: used to check if the connection is on
      case '!':
        Serial.write('!');
      break;
      
      //turns blue LED on
      case 'n':
        fps.SetLED(true);
      break;
      
      //turns blue LED off
      case 'm':
        fps.SetLED(false);
      break;

      //returns the number of enrolled fingerprints on device
      case 'b':
        Serial.print(fps.GetEnrollCount());
      break;

      //checks if a finger ID is in use
      case 'c':
        delay(2);
        if(fps.CheckEnrolled(Serial.read())){
          Serial.print('y');
        }
        else{
          Serial.print('n');
        }
      break;

      //checks if a finger is pressed to the scanner
      case 'd':
        if(fps.IsPressFinger()){
          Serial.print('y');
        }
        else{
          Serial.print('n');
        }
      break;

      //delete a fingerprint of a certain ID
      case 'e':
        delay(2);
        fps.DeleteID(Serial.read());
      break;

      //delete all fingerprints
      case 'f':
        fps.DeleteAll();
      break;
      
      //verify 1:1
      case 'g':
        delay(2);
        fps.CaptureFinger(false);
        int id;
        id=1;
        if(fps.Verify1_1(id)==0){
          char pass[32];
          int i;
          for(i=0;i<32;i++){
            int num;
            num = PIN[i]*31*(id+13);
            char r;
            r = num%255;

            Serial.print(r);
          }
        }
         else{
            int i;
            for(i=0;i<32;i++){
              char z;
              z=0;
            Serial.print(z);
            }
         }
      break;

      //identify 1:N
      case 'h':
      {
        fps.CaptureFinger(false);
        int id = fps.Identify1_N();
        long lid = (long)id;
        if (id < 20){
          int i;
          for(i=0;i<32;i++){
            long num;
            num = PIN[i]*31L*(lid+13L);
            char r;
            r = (num%255);
            Serial.print(r);
          }
        }
        else{
          int i;
          for(i=0;i<32;i++){
              char z;
              z=0;
            Serial.print(z);
          }
        }
      }  
      break;

      //checks if a finger is already scanned
      case 'j':
      {
        fps.CaptureFinger(false);
        int id = fps.Identify1_N();
        int n;
        if (id < 20){
          n=1;
        }
        else{
          n=0;
        }
        Serial.print(n);
      }  
      break;
      

//enrollment

     //enroll start
      case 'q':
      {
        int enrollid = 0;
        bool usedid = true;
        while (usedid == true){
          usedid = fps.CheckEnrolled(enrollid);
          if (usedid==true) enrollid++;
        }
        fps.EnrollStart(enrollid);
        Serial.print('k');
      }
      break;

      //enroll1
      case 'r':
      {
        bool ret = fps.CaptureFinger(true);
        if (!ret){
          Serial.print('n');
          break;
        }
        fps.Enroll1();
        Serial.print('k');
      }
      break;

      //enroll2
      case 's':
      {
        bool ret = fps.CaptureFinger(true);
        if (!ret){
          Serial.print('n');
          break;
        }
        fps.Enroll2();
        Serial.print('k');
      }
      break;

      //enroll3
      case 't':
      {
        bool bret = fps.CaptureFinger(true);
        int iret = fps.Enroll3();
        if (!bret){
          Serial.print('n');
          break;
        }
        if (iret != 0){
          Serial.print('n');
          break;
        }
        Serial.print('k');
      }
      break;

    }
  }
}
