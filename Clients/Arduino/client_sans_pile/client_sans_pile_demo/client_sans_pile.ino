#include "Arduino.h"
#include <aJSON.h>
#include <LiquidCrystal.h>
#include <Ethernet.h>
#include <SPI.h>
#include <WebSocketClient.h>

byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x32, 0x87 }; // Gali 11

//IPAddress server(192,168,1,1); // serveur
IPAddress ip(192,168,1,9); // ip
IPAddress dns(192,168,1,1); // ip
IPAddress gateway(192,168,1,1); // ip
IPAddress subnet(255,255,255,0); // ip

// function definitions
char* parseJsonVertex(char *jsonString) ;
int parseJsonId(char *jsonString) ;
char* parseJsonAvailable(char *jsonString) ;

char trame[] = "{\"vertex\":\"b\",\"id\":\"0\", \"available\":\"false\"}";
char jsonString[] = "{\"query\":{\"count\":1,\"created\":\"2012-08-04T14:46:03Z\",\"lang\":\"en-US\",\"results\":{\"item\":{\"title\":\"Handling FTP usernames with @ in them\"}}}}";
char trame_retour[] = "{\"accepted\":true,\"vertex\":\"a\",\"id\":0}";

char * trameVertex;
int trameId;
char * trameAvailable;
int travelled;

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

  lcd->print(trameVertex); // print a simple message
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

//parsing de la trame(valeur de la distance parcourur)
int parseJsonTraveled(char *jsonString) 
{
    int value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "travelled"); 

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

//parsing de la trame(valeur du vertex)
char* parseJsonAvailable(char *jsonString) 
{
    char* value;

    aJsonObject* root = aJson.parse(jsonString);

    if (root != NULL) {
        //Serial.println("Parsed successfully 1 " );
        aJsonObject* vertex = aJson.getObjectItem(root, "available"); 

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



void loop() {
  client.monitor();
  
  
  
  
  //affichage
  lcd->setCursor(0,0);
  lcd->print("traveled:");
  lcd->print(String(travelled));
  lcd->setCursor(12,0);
  lcd->print("p:");
  lcd->print(0);

  lcd->setCursor(0,1);            // move to the begining of the second line
  lcd_key = read_LCD_buttons();  // read the buttons
  
  //gestion des bouton
  switch (lcd_key)               // depending on which button was pushed, we perform an action
 {
   case btnRIGHT:
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
     
     break;
     }
   case btnLEFT:
     {
     lcd->print("NON   ");
     //client.send("NON");
     //trameVertex=parseJsonVertex(trame);
     //trameId=parseJsonId(trame);
     String  retour = "{\"accepted\":false,"; retour+="\"vertex\":\""; 
     retour+=String(trameVertex); retour+="\",\"id\":";retour+=String(trameId);retour+="}\r\n";
     
     retour.toCharArray(trame_retour,42);
     
     client.send(trame_retour);
     
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
  trameVertex = parseJsonVertex(message);
  trameId = parseJsonId(message);
  trameAvailable = parseJsonAvailable(message);
  travelled = parseJsonTraveled(message);
  
  //on affiche la destination
  lcd->setCursor(8,1);
  lcd->print("dest:");
  lcd->print(trameVertex);
}

void onError(WebSocketClient client, char* message) {
  Serial.println("EXAMPLE: onError()");
  Serial.print("ERROR: "); Serial.println(message);
}


