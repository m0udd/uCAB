#
# This is the main file of PI3A uCAB project:
#
# Basic comunication strategy:
# All clients need a connection with this pyrhon server.
# This server use the flask socket-io (websocket based) protocol 
#
#@author : mingar
#

from flask import *
from flask.ext.socketio import *
from map_manipulation import *
import threading
from fonction_pathfinder import *
import json
import time
import socket

global response
response = []
global inMessage
inMessage = []

TCP_IP = '192.168.1.1'
TCP_PORT = 9741
BUFFER_SIZE = 1024

app = Flask(__name__)
#Don't print HTTP logs
app.logger.disabled = True
    
app.config['SECRET_KEY'] = 'pass'
socketio = SocketIO(app)
thread = False

global server
server = None

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

#
# Flask ------------------------------------------------------------------------
#
    
#This thread is used for moving cab (computation)
def cab_thread():
    #Send an keep alive message every 5 seconds (for tests and debug)
    while True:
        time.sleep(2)
        #Cab motion
        i=0
        for cab in map.cabs:
            if cab['accepted'] == True and cab['position'] != cab['target']:
                #move the cab !
                print 'background_thread -> from ', cab['position'], ' to ', cab['target']
                nextNode = pluscourchemin(cab['position'], cab['target'], map.map)
                #increment the distance since the last course
                cab['travelled'] += 1
                cab['position'] = nextNode
                #Broadcast than that the map changed for all clients
                socketio.emit('new map is available',namespace='/client')
                setCabState(i,False)

            else:
                #end of motion ? update cab
                #target reached
                cab['accepted'] = False
                setCabState(i,True)
                #set the distance since the last course to 0
                cab['travelled'] = 0
                #send the state cab is available
            i+=1
            #print server
        #socketio.emit('log', {'data': 'keep_alive'}, namespace='/client')


#The root URL ------------------------------------------------------------------
@app.route('/')
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
@app.route('/client')
def get_url_of_webservices_clients():    
    return render_template('url.json.html', namespace='client')


#The device URL
@app.route('/cab')
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
            cab['target'] = target
    #Broadcast to the cab
    #cabsWS.broadcastMsg(target)
    broadcastMsgToCabs(target)
 

#
# The CAB WebSocket ------------------------------------------------------------
#
global clients
clients = []

def broadcastMsgToCabs(vertex):
    print 'broadcastMsgToCabs'
    id=0
    resp = { "id" : id,"vertex": vertex, "travelled": map.cabs[id]["travelled"] }
    response.append( resp )
    id += 1

def setCabState(id, state):
    global map
    #print 'snd : ', state
    map.cabs[id]["accepted"] = state
    resp = { "id" : id, "available": state }
    #response.append( resp )

'''
class CabWS(WebSocket):

    def handleMessage(self):
        #the new message
        cabResponse = json.loads(self.data)
        setCabState(cabResponse['id'], cabResponse['accepted'])
        print 'Cab with ID : ', cabResponse['id'], ' response : ', cabResponse['accepted'], \
            ' for vertex : ', cabResponse['vertex']


    def handleConnected(self):
        #the first cab's connection
        print (u'CAB connected : ' + self.address[0])
        global clients
        clients.append(self)

    def handleClose(self):
        print (u'CAB disconnected : ' + self.address[0])
        global clients
        clients.remove(self)
        #the end of ws deconnection
        nb_of_cab-=1
'''
def thread_io():
    socketio.run(app, host='0.0.0.0', port=9740)

#response.append(1)

def thread_tcp_arduino():
    global response
    global inMessage
    arduTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arduTCP.bind(('0.0.0.0', 9741))
    while 1:
        arduTCP.listen(1)
        conn, addr = arduTCP.accept()
        print 'Connection Galileo address:', addr
        response = []
        inMessage = []
        while 1:
            print response
            if len(response) > 0:
                conn.send( json.dumps(response[0])+"\r\n" )
                response.pop(0)
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            if data.find("loop") is not 0:
                inMessage.append(data)
        conn.close()


if __name__ == '__main__':

    print 'Server cab thread !'
    cabThread = threading.Thread(target = cab_thread)
    cabThread.start()

    print 'Server FlaskIO start !'
    ioThread = threading.Thread(target = thread_io)
    ioThread.start()

    print 'Server Cab start !'
    socketThread = threading.Thread(target = thread_tcp_arduino)
    socketThread.start()

    print 'Server stop, wait for all threads to terminate...'
    cabThread.join()
