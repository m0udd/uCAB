//
//  Client.swift
//  graphique
//
//  Created by Rémi LAVIELLE on 20/10/2015.
//  Copyright © 2015 Rémi LAVIELLE. All rights reserved.
//

import Foundation
import Socket_IO_Client_Swift
import SwiftyJSON



public class Client : WebSocketDelegate
{
    
    var name: String
    var message: String = ""
    var cercle = [CGPoint(x:0, y:0)]
    
    let mySocket=SocketIOClient(socketURL: "192.168.2.1:9740")
    
    init(name: String = "John Doe")
    {
        self.name = name
        connexionServeur()
        topic()
        addNewMap()
    }
    
    func connexionServeur()
        
    {
        self.mySocket.connect()
        print("Connexion reussit")
    }
    
    func addNewMap()
    {
        self.mySocket.on("new map")
            {
                data, ack in
                
                // On parse la reponse en chaine de caractère
                self.message = data[0] as! String
                print(self.message)
                
                if let test = self.message.dataUsingEncoding(NSUTF8StringEncoding)
                {
                    print(" ")
                    let json = JSON(data: test)
                    
                    // On récupère la taille des éléments
                    let taille = json["map"]["vertices"].count
                    
                    print(taille)
                    print("")
                    
                    
                    for item in json["map"]["vertices"].arrayValue
                    {
                        let test = item["x"].floatValue
                        print(test+2)
                        
                    }
                }
        }
    }
    
    func sendNeedMap()
    {
        self.mySocket.emit("get my map")
    }
    
    func topic()
    {
        self.mySocket.joinNamespace("/client")
    }
    
    func dialogueServeur()
    {
        sendNeedMap()
    }
    
    func ajoutCoordPoint()
    {
        
    }
    
    public func websocketDidConnect(socket: WebSocket) {
        print("websocket is connected")
    }
    
    public func websocketDidDisconnect(socket: WebSocket, error: NSError?) {
        print("websocket is disconnected: \(error?.localizedDescription)")
    }
    
    public func websocketDidReceiveMessage(socket: WebSocket, text: String) {
        print("got some text: \(text)")
    }
    
    public func websocketDidReceiveData(socket: WebSocket, data: NSData) {
        print("got some data: \(data.length)")
    }
    
}
