#
# Base class for websocket communiction between raspi and gallileo
#
#@author : mingar
#

from flask import *
from flask.ext.socketio import *
from map_manipulation import *
from threading import Thread
import json
import time
from fonction_pathfinder import *
from cab_websocket import *
from SimpleWebSocketServer import *
import signal
import sys
import threading

app = Flask(__name__)
#Don't print HTTP logs
app.logger.disabled = True
    
app.config['SECRET_KEY'] = 'pass'
socketio = SocketIO(app)
thread = None


#it's ugly, TODO : fix it!
global nb_of_cab
nb_of_cab = 0
global map 
map = MapManager()
#List for 3 available clients slot 
global clients_slots
clients_slots = [True,True,True]

#
# Websocket for Galileo --------------------------------------------------------
#

def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


#
# Flask ------------------------------------------------------------------------
#
    
#This thread is used for moving cab (computation)
def background_thread():
    #Send an keep alive message every 5 seconds (for tests and debug)
    while True:
        time.sleep(2)
        #Cab motion
        for cab in map.cabs:
            if cab['accepted'] == True and cab['position'] != cab['target']:
                #move the cab !
                print 'background_thread -> from ', cab['position'], ' to ', cab['target']
                nextNode = pluscourchemin(cab['position'], cab['target'], map.map)                
                cab['travelled'] += 1
                cab['position'] = nextNode                
                #Broadcast than that the map changed for all clients
                socketio.emit('new map is available',namespace='/client')
                
            else:
                #end of motion ? update cab
                #target reached
                cab['accepted'] = False
                cab['available'] = True
                cab['travelled'] = 0
        #socketio.emit('log', {'data': 'keep_alive'}, namespace='/client')


#The root URL ------------------------------------------------------------------
@app.route('/client')
def index():    
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    template = 'index.html'
    #Too many clients?
    if clients_slots[0] == False and clients_slots[1] == False and clients_slots[2] == False:
        template = 'too_many.html'
    return render_template(template)


#The device URL
@app.route('/clientsio')
def get_url_of_webservices_clients():    
    return render_template('url.json.html', namespace='client')


#The device URL
@app.route('/cabsio')
def get_url_of_webservices_cab():    
    return render_template('url.json.html', namespace='cab')

#
# The client SocketIO ----------------------------------------------------------
#

#the sio connection
@socketio.on('connect', namespace='/client')
def client_connect():
    for i in range(0,3):
        if clients_slots[i] == True:
            print 'Client connected, ID : ', i
            session['id'] = i
            clients_slots[i] = False
            i = -1
            break
    if i != -1:
        print 'Too many client connected'
        #TODO Close socket 
    if clients_slots[0] == False and clients_slots[1] == False and clients_slots[2] == False:
            emit('new map is available', broadcast=True)
        

#the end of sio deconnection
@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    clients_slots[int(session.get('id', 0))] = True;
    print('Client disconnected, ID : ' + str(session.get('id', 0)))


#the client wishes receive its map   
@socketio.on('get my map', namespace='/client')
def client_get_map():
    if clients_slots[0] == False and clients_slots[1] == False and clients_slots[2] == False:
        emit('new map', json.dumps( map.get_map(int(session.get('id', 0))) ))
    else:
        emit('no map', {'data': "The server have not 3 clients! sorry... :( ", 'isOk': False})


#the client called a cab
@socketio.on('new target', namespace='/client')
def client_set_new_target(message):    
    target = cabineplusproche( message['x'], message['y'], map.map, int(session.get('id', 0)))
    #Set one available the cab
    for cab in map.cabs:
        if(cab['available'] == True):
            cab['accepted'] = True #TODO fix it
            cab['target'] = target
    #Broadcast to the cab
    broadcastMsgToCabs({'target': target}) 
 

#
# The CAB WebSocket ------------------------------------------------------------
#


clients = []
def broadcastMsgToCabs(msg):
        print 'broadcastMsg'
        id=0
        for client in list(clients):
            id+=1
            print 'Client : ', client
            response = { "id" : id,"vertex": "a", "available":True }
            client.sendMessage( unicode(json.dumps(response)) )

class CabWS(WebSocket):

    def handleMessage(self):
        #the new message
        print 'handleMessage'
        for client in list(clients):
            print self.data
            if client != self:
                print (self.address[0] + ' - ' + self.data)

    def broadcastMsg(self, msg):
        #the first cab's connection
        print 'broadcastMsg'
        for client in list(clients):
            client.sendMessage(msg)

    def handleConnected(self):
        #the first cab's connection
        print 'handleConnected'
        print (u'CAB connected : ' + self.address[0])
        clients.append(self)
        self.broadcastMsg( unicode("{\"vertex\":\"b\",\"id\":\"0\", \"available\":\"false\"}") )

    def handleClose(self):
        #the end of ws deconnection
        print 'handleClose'
        clients.remove(self)
        print (u'CAB disconnected : ' + self.address[0])
        nb_of_cab-=1

"""
#the cab agrees to retrieve client
@socketio.on('cab ok', namespace='/cab')
def client_set_new_target(message):
    cab_id = int(session.get('id', 0))
    x_target = message['x']
    y_target = message['y']
    print 'New target, cab with ID :', cab_id, 'set X = ', x_target, ' Y = ', y_target
    #TODO compute vertice
    #vertice_to_go = 
    #map.set_cab_state(cab_id, False, True, +1, vertice_to_go )
    #set the distance since the last course to 0
    #map.set_cab_travelled(cab_id, 0, 0)
    #Broadcast than that the map changed for all clients
"""

def thread_flask():
    socketio.run(app, host='0.0.0.0', port=9740)
    

if __name__ == '__main__':

    #Init SIGINT
    """
    def close_sig_handler(signal, frame):
        if server:
            server.close()
        if socketio.server:
            socketio.server.stop();
        sys.exit()


    signal.signal(signal.SIGINT, close_sig_handler)
    """

    print 'Server start !'
    cabsWS = CabWS

    server = SimpleWebSocketServer('', 9741, cabsWS)

    print 'Start Flask SocketIO server !'
    t1 = threading.Thread(target = thread_flask)
    t1.start()

    print 'Server WS Cab start !'
    server.serveforever()

    print 'Server stop !'
    t1.join()
    
    

     
