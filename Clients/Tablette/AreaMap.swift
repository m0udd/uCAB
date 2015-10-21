//
//  demo.swift
//  graphique
//
//  Created by Rémi LAVIELLE on 19/10/2015.
//  Copyright © 2015 Rémi LAVIELLE. All rights reserved.
//

import Foundation
import UIKit

class AreaMap: UIView
{
    // Tableau de point
    var points = [CGPoint(x:50, y:50)]
    
    
    // Position premier point
    let pointSize = CGSize(width: 30, height: 30)
   
    // fonction de dessin surdefini
    override func drawRect(rect: CGRect)
    {
        
        
        // Couleur de depart
        UIColor.whiteColor().set()
        
        // on remplit la vue
        UIRectFill(self.bounds)
        
        // Création de la ligne
        let ligne = UIBezierPath()
        
        // Premier Point de la droite
        var temp = CGPoint(x:50,y:50)
        
        
        //On affiche a ce point
        ligne.moveToPoint(temp)
        
        // Boucle pour chaque points
        for point in points
        {
           
            // On choisit la couleur rouge
            UIColor.redColor().set()
            
            // On crer bien le cercle au centre du point
            let p = CGPoint(
                x: point.x - pointSize.width/2,
                y: point.y - pointSize.height/2
            )
            
            // On dessine le cercle
            let cercle = UIBezierPath(ovalInRect: CGRect(origin:p, size:pointSize))
            cercle.fill()
            
            //ON affiche les points
            print (points)
            
            // Coloration de la ligne
            UIColor.blackColor().set()

            // On relie le premier point au second
            ligne.addLineToPoint(point)
            
            // On récupere les coordonnees du point précedent
            temp=point
        }
        
        //On trace la ligne
        ligne.stroke()
    }

}