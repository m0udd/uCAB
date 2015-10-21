#include "Arduino.h"
#include <aJSON.h>
#include <LiquidCrystal.h>
#include <Ethernet.h>
#include <SPI.h>
#include <WebSocketClient.h>
//#include <StackArray.h>
#include <QueueArray.h>

byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x32, 0x87 }; // Gali 11

//IPAddress server(192,168,1,1); // serveur
IPAddress ip(192,168,1,9); // ip
IPAddress dns(192,168,1,1); // ip
IPAddress gateway(192,168,1,1); // ip
IPAddress subnet(255,255,255,0); // ip

// declaration des fonction de parsing JSON
char* parseJsonVertex(char *jsonString) ;
int parseJsonId(char *jsonString) ;
int parseJsonTraveled(char *jsonString) ;
   
//exemple de trame                            
char trame[] = "{\"vertex\":\"b\",\"id\":\"0\", \"traveled\":\"10\"}";
char jsonString[] = "{\"query\":{\"count\":1,\"created\":\"2012-08-04T14:46:03Z\",\"lang\":\"en-US\",\"results\":{\"item\":{\"title\":\"Handling FTP usernames with @ in them\"}}}}";
char trame_retour[] = "{\"accepted\":false,\"vertex\":\"a\",\"id\":9}";
char* msg;

//variable contenant les elements des trames
char * trameVertex;
int trameId;
int trameTraveled=0;
char * trameAvailable="true";

//la file d'attente des demandes pour le taxi
QueueArray <char*> stack; 

//on delcare l'adresse du serveur et le port d'ecoute
char server[] = "192.168.1.1";
int port = 9741;

WebSocketClient client;

// select the pins used on the LCD panel
LiquidCrystal * lcd;

// define some values used by the panel and buttons
int lcd_key     = 0;
int adc_key_in  = 0;
#define btnRIGHT  0
#define btnUP     1
#define btnDOWN   2
#define btnLEFT   3
#define btnSELECT 4
#define btnNONE   5

// read the buttons
int read_LCD_buttons()
{
 adc_key_in = analogRead(0);      // read the value from the sensor 
 // my buttons when read are centered at these valies: 0, 144, 329, 504, 741
 // we add approx 50 to those values and check to see if we are close
 if (adc_key_in > 1000) return btnNONE; // We make this the 1st option for speed reasons since it will be the most likely result
 // For V1.1 us this threshold
 if (adc_key_in < 50)   return btnRIGHT;  
 
 if (adc_key_in < 650)  return btnLEFT; 
 
 if (adc_key_in < 790)  return btnSELECT;
  

 return btnNONE;  // when all others fail, return this...
}



void setup() {
  
  // select the pins used on the LCD panel
  lcd = new LiquidCrystal(8, 9, 4, 5, 6, 7);
  
  lcd->begin(16, 2);              // start the library
  lcd->setCursor(0,0);
  

  
  system("ifconfig > /dev/ttyGS0");
  Serial.begin(9600);
  delay(1000);
  // start the Ethernet connection:
  Ethernet.begin(mac,ip,dns,gateway,subnet); 
  // give the Ethernet shield a second to initialize:
  delay(1000);
  
  Serial.println("connecting...");
  Serial.println("EXAMPLE: setup()");

  client.connect(server,port);
  client.onOpen(onOpen);
  client.onMessage(onMessage);
  client.onError(onError);

  
}


//parsing de la trame(valeur du vertex)
char* parseJsonVertex(char *jsonString) 
{
    char* value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "vertex"); 

             if (vertex != NULL) {
                 //Serial.println("Parsed successfully 5 " );
                 value = vertex->valuestring;
             }
    }

    if (value) {
        return value;
    } else {
        return NULL;
    }
}


//parsing de la trame(valeur de l'id)
int parseJsonId(char *jsonString) 
{
    int value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "id"); 

             if (vertex != NULL) {
                 //Serial.println("Parsed successfully 5 " );
                 value = vertex->valueint;
             }
    }

    if (value) {
        return value;
    } else {
        return NULL;
    }
}

//parsing de la trame(valeur de la distance parcourur)
int parseJsonTraveled(char *jsonString) 
{
    int value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "traveled"); 

             if (vertex != NULL) {
                 //Serial.println("Parsed successfully 5 " );
                 value = vertex->valueint;
             }
    }

    if (value) {
        return value;
    } else {
        return NULL;
    }
}

//parsing de la trame(valeur du vertex)
char * parseJsonAvailable(char *jsonString) 
{
    char* value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "traveled"); 

             if (vertex != NULL) {
                 //Serial.println("Parsed successfully 5 " );
                 value = vertex->valuestring;
             }
    }

    if (value) {
        return value;
    } else {
        return NULL;
    }
}


//fonction loop
//la fonction rappelé à chaque fois
void loop() {
  client.monitor();
  
  
  lcd->setCursor(0,0);
  lcd->print("traveled:");
  lcd->print(trameTraveled);
  lcd->setCursor(12,0);
  lcd->print("p:");
  lcd->print(String(trameTraveled));
  
  //gestion des bouton
  
  
  lcd->setCursor(0,1);            // move to the begining of the second line
  lcd_key = read_LCD_buttons();  // read the buttons
  
  
  
  switch (lcd_key)               // depending on which button was pushed, we perform an action
 {
   case btnRIGHT:
     {
       if(trameAvailable="true")
       {
             lcd->print("OUI ");
         //client.send("OUI");
         //char trame_retour[] = {"accepted":true,"vertex":"a","id":0}
         //trameVertex=parseJsonVertex(trame);
         //trameId=parseJsonId(trame);
         
         String  retour = "{\"accepted\":true,"; retour+="\"vertex\":\""; 
         retour+=String(trameVertex); retour+="\",\"id\":";retour+=String(trameId);retour+="}\r\n";
         
         retour.toCharArray(trame_retour,42);
         
         client.send(trame_retour);
         
         msg = new char[255]; 
         msg = stack.pop(); 
      
         trameVertex = parseJsonVertex(msg);
         trameId = parseJsonId(msg);
         trameAvailable = parseJsonAvailable(msg);
         
         lcd->setCursor(9,1);            // move cursor to second line "1" and 9 spaces over
         //lcd->print(millis()/1000);      // display seconds elapsed since power-up
         lcd->print("Pile:");
         lcd->setCursor(15,1);
         lcd->print(String(stack.count()));  
       }
       else
       {
       lcd->print("non disponible");
       }
     
     
     break;
     }
   case btnLEFT:
     {
       if(trameAvailable="true")
       {
         lcd->print("NON   ");
         //client.send("NON");
         //trameVertex=parseJsonVertex(trame);
         //trameId=parseJsonId(trame);
         
         String  retour = "{\"accepted\":false,"; retour+="\"vertex\":\""; 
         retour+=String(trameVertex); retour+="\",\"id\":";retour+=String(trameId);retour+="}\r\n";
         
         retour.toCharArray(trame_retour,42);
         
         client.send(trame_retour);
         
         msg = new char[255]; 
         msg = stack.pop(); 
      
         trameVertex = parseJsonVertex(msg);
         trameId = parseJsonId(msg);
         trameAvailable = parseJsonAvailable(msg);
         
         lcd->setCursor(9,1);            // move cursor to second line "1" and 9 spaces over
         //lcd->print(millis()/1000);      // display seconds elapsed since power-up
         lcd->print("Pile:");
         lcd->setCursor(15,1);
         lcd->print(String(stack.count()));  
       }
       else
       {
       lcd->print("non disponible");
       }
     break;
     }
     
     case btnSELECT:
     {
       
     lcd->setCursor(9,1);            // move cursor to second line "1" and 9 spaces over
     //lcd->print(millis()/1000);      // display seconds elapsed since power-up
     lcd->print("Pile:");
     lcd->setCursor(15,1);
     lcd->print(String(stack.count()));  
       
     msg = new char[255]; 
     msg = stack.pop(); 
  
     trameVertex = parseJsonVertex(msg);
     trameId = parseJsonId(msg);
     trameAvailable = parseJsonAvailable(msg);
  
     
     break;
     }
 }
  
}

void onOpen(WebSocketClient client) {
  Serial.println("EXAMPLE: onOpen()");
}

void onMessage(WebSocketClient client, char* message) {
  Serial.println("EXAMPLE: onMessage()");
  Serial.print("Received: "); Serial.println(message);
 
  //on parse direct
  trameVertex = "";
  trameVertex = parseJsonVertex(message);
  trameId = parseJsonId(message);
  trameTraveled = parseJsonTraveled(message);
  trameAvailable = parseJsonAvailable(message);
  
  //on affiche la destinarion sur l'ecran lcd
  lcd->setCursor(0,1);
  lcd->print("destination:");
  lcd->setCursor(13,0);  
  lcd->print(trameVertex);
  
  //on stock le message dans la pile
  if(trameVertex != "")
  {
    stack.push(message);
  }
  
  
  
}

void onError(WebSocketClient client, char* message) {
  Serial.println("EXAMPLE: onError()");
  Serial.print("ERROR: "); Serial.println(message);
}


