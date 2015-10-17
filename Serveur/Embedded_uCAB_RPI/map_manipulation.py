#
# This file contins all methods for map manipulation
#
#@author : mingar
#

import json

class MapManager:
    
    def __init__(self):
        self.map = [{
            "areas": [
                {
                    "name": "Quartier Nord",
                    "map": {
                        "weight": {
                            "w": 1,
                            "h": 1
                        },
                        "vertices": [
                            {
                                "name": "m",
                                "x": 0.5,
                                "y": 0.5
                            },
                            {
                                "name": "b",
                                "x": 0.5,
                                "y": 1
                            }
                        ],
                        "streets": [
                            {
                                "name": "mb",
                                "path": [
                                    "m",
                                    "b"
                                ],
                                "oneway": False
                            }
                        ],
                        "bridges": [
                            {
                                "from": "b",
                                "to": {
                                    "area": "Quartier Sud",
                                    "vertex": "h"
                                },
                                "weight": 2
                            }
                        ],
                        "cabs":[
                            {
                                "available": False,
                                "moving": False,
                                "position": 
                                {
                                    "vertice": "m",
                                }, 
                                "target": 
                                {
                                    "vertice": "a",
                                }, 
                                "travelled": 
                                {
                                    "vertice": 1,
                                }
                            }]
                    }
                    
                }, 
                {
                    "name": "Quartier Sud",
                    "map": {
                        "weight": {
                            "w": 1,
                            "h": 1
                        },
                        "vertices": [
                            {
                                "name": "a",
                                "x": 1,
                                "y": 1
                            },
                            {
                                "name": "m",
                                "x": 0,
                                "y": 1
                            },
                            {
                                "name": "h",
                                "x": 0.5,
                                "y": 0
                            }
                        ],
                        "streets": [
                            {
                                "name": "ah",
                                "path": [
                                    "a",
                                    "h"
                                ],
                                "oneway": False
                            },
                            {
                                "name": "mh",
                                "path": [
                                    "m",
                                    "h"
                                ],
                                "oneway": False
                            }
                        ],
                        "bridges": [
                            {
                                "from": "h",
                                "to": {
                                    "area": "Quartier Nord",
                                    "vertex": "b"
                                },
                                "weight": 2
                            }
                        ],
                        "cabs":[
                            {
                                "available": False,
                                "moving": False,
                                "position": 
                                {
                                    "vertice": "m",
                                }, 
                                "target": 
                                {
                                    "vertice": "a",
                                }, 
                                "travelled": 
                                {
                                    "vertice": 1,
                                }
                            }]
                    }
                },
                {
                    "name": "Quartier Est",
                    "map": {
                        "weight": {
                            "w": 1,
                            "h": 1
                        },
                        "vertices": [
                            {
                                "name": "a",
                                "x": 0.75,
                                "y": 0.65
                            },
                            {
                                "name": "i",
                                "x": 0.55,
                                "y": 1
                            }
                        ],
                        "streets": [
                            {
                                "name": "ai",
                                "path": [
                                    "a",
                                    "i"
                                ],
                                "oneway": False
                            }
                        ],
                        "bridges": [
                            {
                                "from": "i",
                                "to": {
                                    "area": "Quartier Sud",
                                    "vertex": "h"
                                },
                                "weight": 2
                            }
                        ]
                    }
                }
            ]            
        }]

    #Convert all json to a string
    def json_to_str_map(self):
        return json.dumps(self.map[0], ensure_ascii=False)

    #Convert only a user json to a string    
    def json_to_str_map(self, id):
        if id > len(self.map[0]['areas']):
            id = len(self.map[0]['areas'])
        return json.dumps(self.map[0]['areas'][id], ensure_ascii=False)

    def set_cab_state(self, id, isAvailable, isMoving, addToQueue, vertice_to_go):
        #update the cab's state 
        self.map[0]['cabs'][id]['available'] = isAvailable
        self.map[0]['cabs'][id]['moving'] = isMoving
        self.map[0]['cabs'][id]['queue'] = self.map[0]['cabs'][id]['queue'] + addToQueue
        #update the traget    
        self.map[0]['cabs'][id]['target']['vertice'] = vertice_to_go

    def set_cab_position(self, id, vertice):
        self.map[0]['cabs'][id]['position']['vertice'] = vertice


    def set_cab_target(self, id, vertice):
        self.map[0]['cabs'][id]['target']['vertice'] = vertice


    def set_cab_travelled(self, id, vertice):
        #set the distance since the last course to 0
        self.map[0]['cabs'][id]['travelled']['vertice'] = vertice


    def print_all_cab(self):
        print '---'
        print self.map[0]['cabs']
        print '---'

    def getMap(self, id):
        return self.map[0]['areas'][id]