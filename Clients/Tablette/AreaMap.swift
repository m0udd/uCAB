//
//  demo.swift
//  graphique
//
//  Created by Rémi LAVIELLE on 19/10/2015.
//  Copyright © 2015 Rémi LAVIELLE. All rights reserved.
//

import Foundation
import UIKit
import Socket_IO_Client_Swift
import SwiftyJSON


class AreaMap: UIView
{
    
    // Tableau de point
    var points = [CGPoint(x:0, y:0)]
    
    // Dimension du point
    let pointSize = CGSize(width: 30, height: 30)
    
    // INstenciation objet client
    let monClient = Client()
    
    ///////////////////////////////////////////////////////////////////////////////////////////////
    
    // GRAPHIQUE
    
   ///////////////////////////////////////////////////////////////////////////////////////////////
    
    
    // fonction de dessin surdefini
    override func drawRect(rect: CGRect)
    {
        monClient.dialogueServeur()
        remplirTablleau(monClient.cercle)
        
        
        
        
    }
    
    /////////////////////////////////////////////////////////////////////////
    
    // FONCTIONS
    
    /////////////////////////////////////////////////////////////////////////
    
    
    func remplirTablleau(tableau: [CGPoint]) -> [CGPoint]
    {
        for var i = 0; i<self.monClient.cercle.capacity; i++
        {
            let q = CGPoint(
                x: self.monClient.cercle[i].x - pointSize.width/2,
                y: self.monClient.cercle[i].y - pointSize.height/2)
            

            points[i].x = q.x
            points[i].y = q.y
            print(points[i].x)
            print(points[i].y)
            
        }
        
        print("cont")
        print(points.capacity)
        
        return points
    }
    

}