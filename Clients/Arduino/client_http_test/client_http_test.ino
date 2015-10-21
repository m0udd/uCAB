#include "Arduino.h"
#include <aJSON.h>
#include <LiquidCrystal.h>
#include <SPI.h>
#include <Ethernet.h>

// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
//byte mac[] = {  0x98, 0x4F, 0xEE, 0x05, 0x34, 0x14 };
byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x32, 0x87 }; // Gali 11
//IPAddress server(173,194,33,104); // Google
IPAddress server(192,168,1,1); // serveur

IPAddress ip(192,168,1,9); // ip

IPAddress dns(192,168,1,1); // ip
IPAddress gateway(192,168,1,1); // ip
IPAddress subnet(255,255,255,0); // ip

// Initialize the Ethernet client library
// with the IP address and port of the server 
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;

// declaration des fonction de parsing JSON
char* parseJsonVertex(char *jsonString) ;
int parseJsonId(char *jsonString) ;
int parseJsonTraveled(char *jsonString) ;


//exemple de trame                            
char trame[] = "{\"vertex\":\"b\",\"id\":\"0\", \"traveled\":\"10\"}";
char jsonString[] = "{\"query\":{\"count\":1,\"created\":\"2012-08-04T14:46:03Z\",\"lang\":\"en-US\",\"results\":{\"item\":{\"title\":\"Handling FTP usernames with @ in them\"}}}}";
char trame_retour[] = "{\"accepted\":false,\"vertex\":\"a\",\"id\":9}";
char message[255];

//variable contenant les elements des trames
char * trameVertex;
int trameId=0;
int trameTraveled=0;
char * trameAvailable="true";
String trameStr="";

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
  
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
  delay(1000);
  
   while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // start the Ethernet connection:
  /*if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    for(;;)
      ;
  }*/
  
  delay(1000);
    // start the Ethernet connection:
  Ethernet.begin(mac,ip,dns,gateway,subnet); 

  
  
  
  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 9741)) {
    Serial.println("connected");
    // Make a HTTP request:
    client.print("{\"id\":0,\"available\":true}\r\n");
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
   //system("ifconfig > /dev/ttyGS0");
  //Serial.println(Ethernet.localIP());
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

void loop()
{
  client.print("loop\r\n");
  delay(2000);
  
  //affichage
  lcd->setCursor(0,0);
  lcd->print("traveled:");
  lcd->print(trameTraveled);
  lcd->setCursor(12,0);
  lcd->print("p:");
  lcd->print(0);
  
  
  //si le client est connecté
  if(client.connected()){
    //Serial.println("Loop : connected == true");
    //Serial.println("ClientConnected");
    //si il y a des données a lire ...
    while(client.available()) {
      //Serial.println("Loop : Données disponibles !");
      char c = client.read();
      Serial.print(c);
      
      trameStr+=c;
      
    }
    Serial.println("trameStr:");
    Serial.print(trameStr);
    //on a recuperer le msg, on le parse
  
    trameStr.toCharArray(message,255);
    Serial.print("message:");
    Serial.println(message);
    trameVertex = parseJsonVertex(message);
    Serial.print("vertex:");
    Serial.println(trameVertex);
    trameId = parseJsonId(message);
    Serial.print("id:");
    Serial.println(trameId);
    trameTraveled = parseJsonTraveled(message);
    Serial.print("traveled:");
    Serial.println(trameTraveled);
    trameAvailable = parseJsonAvailable(message);
    Serial.print("available:");
    Serial.println(trameAvailable);
    
    lcd->setCursor(8,1);
    lcd->print("dest:");
    lcd->print(trameVertex);
    
  }
  
  //si deconnexion
  else {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();

    // do nothing forevermore:
    for(;;)
      ;
  }
  
  switch (lcd_key)               // depending on which button was pushed, we perform an action
 {
   case btnRIGHT:
     {
     lcd->setCursor(0,1);
     lcd->print("OUI ");
     Serial.println("OUI");
     //client.send("OUI");
     //char trame_retour[] = {"accepted":true,"vertex":"a","id":0}
     //trameVertex=parseJsonVertex(trame);
     //trameId=parseJsonId(trame);
     String  retour = "{\"accepted\":true,"; retour+="\"vertex\":\""; 
     retour+=String(trameVertex); retour+="\",\"id\":";retour+=String(trameId);retour+="}\r\n";
     
     Serial.println("message retour");
     Serial.println(retour);
     retour.toCharArray(trame_retour,42);
     Serial.println("trame retour");
     Serial.println(trame_retour);
     client.print(trame_retour);
     
     
     break;
     }
   case btnLEFT:
     {
     lcd->setCursor(0,1);
     lcd->print("NON   ");
     Serial.println("NON");
     //client.send("NON");
     //trameVertex=parseJsonVertex(trame);
     //trameId=parseJsonId(trame);
     String  retour = "{\"accepted\":false,"; retour+="\"vertex\":\""; 
     retour+=String(trameVertex); retour+="\",\"id\":";retour+=String(trameId);retour+="}\r\n";
     
     Serial.println("message retour");
     Serial.println(retour);
     retour.toCharArray(trame_retour,42);
     Serial.println("trame retour");
     Serial.println(trame_retour);
     client.print(trame_retour);
     
     break;
     }
 }
}

