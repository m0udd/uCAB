//
//  ViewController.swift
//  graphique
//
//  Created by Rémi LAVIELLE on 19/10/2015.
//  Copyright © 2015 Rémi LAVIELLE. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    let monClient = Client()
    
    @IBAction func Connexion(sender: AnyObject) {
        
        monClient.dialogueServeur()
    }
    
    // A chaque clic de la souris sur la surface aréa
    @IBAction func tap(sender: UITapGestureRecognizer) {
        
        // On affiche les cordonnes de notre tableau de point fait par la souris
        areaMap.points.append(
            sender.locationInView(areaMap)
        )
        
        // Rafraichissement de la vue
        areaMap.setNeedsDisplay()
    }
    
    @IBOutlet weak var areaMap: AreaMap!
}

