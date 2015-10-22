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
import UIKit



public class Client
{
    
    var name : String = ""
    
    // Dimension du point
    let pointSize = CGSize(width: 30, height: 30)
    
    
    var message: String = ""
    public var cercle = [CGPoint(x: 0.0, y: 0.0)]
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
                self.ajoutCoordPoint(self.message)
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
    
    
    func ajoutCoordPoint(message: String)
    {
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
                var i : Int = 0
                let axeX = item["x"].floatValue
                let axeY = item["y"].floatValue
                
                let coordX = self.reDimensionnementX(axeX)
                let coordY = self.reDimensionnementX(axeY)
                
                print(coordX)
                print(coordY)
                
                cercle[i].x = CGFloat(coordX)
                cercle[i].y = CGFloat(coordY)
                
                
                let newPoint = CGPoint(x: cercle[i].x, y: cercle[i].y)
                let newCercle = UIBezierPath(ovalInRect: CGRect(origin: newPoint, size: pointSize))
                newCercle.fill()
                
                
                i++
            }
            
        }
        
    }
    
    
    func reDimensionnementX(nombreX: Float)->Float
    {
        let maxServeur : Float = 1
        let maxTablette  : Float = 750
        
        let resultAxeX : Float = (nombreX * maxTablette) / maxServeur
        
        return resultAxeX
        
    }
    
    
    func reDimensionnementY(nombreY: Float)->Float
    {
        let maxServeur : Float = 1
        let maxTablette  : Float = 1000
        
        let resultAxeY : Float = (nombreY * maxTablette) / maxServeur
        
        return resultAxeY
    }
    
    

}
