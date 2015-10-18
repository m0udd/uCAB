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
from threading import Thread
import time

app = Flask(__name__)
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


#This thread is used for moving cab (computation)
def background_thread():
    #Send an keep alive message every 5 seconds (for tests and debug)
    while True:
        time.sleep(5)
        #TODO : cab motion
        #if vertice to go is != vertice actual
        #Broadcast than that the map changed for all clients
        #emit('new map is available', broadcast=True)
        #end of motion ? update cab
        socketio.emit('log', {'data': 'keep_alive'}, namespace='/client')


#The root URL
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
# The client SocketIO
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
        emit('new map', map.get_map(int(session.get('id', 0))))
    else:
        emit('no map', {'data': "The server have not 3 clients! sorry... :( ", 'isOk': False})


#the client called a cab
@socketio.on('new target', namespace='/client')
def client_set_new_target(message):
    x_target = message['x']
    y_target = message['y']
    #print 'New target, client with ID :', str(session.get('id', 0)), 'set X = ', x_target, ' Y = ', y_target
    #Broadcast to the cab
    socketio.emit('new destination', {'x': x_target, 'y': y_target}, namespace='/cab') 
 

#
# The cab SocketIO
#

#the first cab's connection
@socketio.on('connect', namespace='/cab')
def client_connect():
    global nb_of_cab    
    session['id'] = nb_of_cab 
    print('Cab connected, ID : ' + str(nb_of_cab))    
    nb_of_cab += 1
 
 
#the end of sio deconnection
@socketio.on('disconnect', namespace='/cab')
def client_disconnect():
    global nb_of_cab
    nb_of_cab -= 1
    print('Cab disconnected, ID : ' + str(session.get('id', 0)))


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
    emit('new map is available', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
