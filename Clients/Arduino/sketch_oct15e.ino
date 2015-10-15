/*
  Web client
 
 
 */

#include <SPI.h>
#include <Ethernet.h>


byte mac[] = { 0x98, 0x4F, 0xEE, 0x05, 0x37, 0xB5 };


IPAddress server(192,168,1,1); // serveur
IPAddress ip(192,168,1,127); // ip
IPAddress dns(192,168,1,1); // dns
IPAddress gateway(192,168,1,1); // gateway
IPAddress subnet(255,255,255,0); // subnet


EthernetClient client;

void setup() {
  
  //system("/etc/init.d/networking restart"); 
  
//system("ifdown eth0");
  //system("ifup eth0");
  //system("ifup eth0");
  //delay(3000);

  system("ifconfig > /dev/ttyGS0");
  
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
   while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

 
    // start the Ethernet connection:
  Ethernet.begin(mac,ip,dns,gateway,subnet); 

 
  
  
  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 5000)) {
    Serial.println("connected");
    // Make a HTTP request:
    client.println("GET / HTTP/1.1");
    client.println();
  } 
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
   system("ifconfig > /dev/ttyGS0");
  Serial.println(Ethernet.localIP());
}

void loop()
{
  delay(2000);
  //si le client est connecté
  if(client.connected()){
    //Serial.println("Loop : connected == true");
    Serial.println("ClientConnected");
    //si il y a des données a lire ...
    if (client.available()) {
      //Serial.println("Loop : Données disponibles !");
      char c = client.read();
      Serial.print(c);
    }
    
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
}

