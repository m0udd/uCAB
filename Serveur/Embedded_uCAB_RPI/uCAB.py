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

#it's ugly, todo : fix it!
global nb_of_client
nb_of_client = 0
global nb_of_cab
nb_of_cab = 0
global map 
map = MapManager()

#This thread is used for moving cab (computation)
def background_thread():
    #Send an keep alive message every 5 seconds (for tests and debug)
    while True:
        time.sleep(5)
        #todo : cab motion
        #Broadcast than that the map changed for all clients
        #emit('new map is available', broadcast=True)
        #end of motion ? update cab
        socketio.emit('log',{'data': 'keep_alive'},namespace='/client')


#The root URL
@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

#
# The client SocketIO
#

#the first sio connection
@socketio.on('connect', namespace='/client')
def client_connect():
    global nb_of_client    
    session['id'] = nb_of_client    
    print('Client connected, ID : ' + str(nb_of_client))
    nb_of_client+=1


#the end of sio deconnection
@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    global nb_of_client
    nb_of_client-=1
    print('Client disconnected, ID : ' + str(session.get('id', 0)))


#the client wishes receive its map   
@socketio.on('get my map', namespace='/client')
def client_get_map():
    if nb_of_client == 3:
        emit('new map', {'data': json_to_str_map(session.get('id', 0)), 'isOk': True})
    elif nb_of_client > 3:
        emit('new map', {'data': "The server have more than 3 clients! sorry... :( ", 'isOk': False})
    else:        
        emit('new map', {'data': "The server have less than 3 clients! sorry... :( ", 'isOk': False})


#the client called a cab
@socketio.on('new target', namespace='/client')
def client_set_new_target(message):
    x_target = message['x']
    y_target = message['y']
    print 'New target, client with ID :', session.get('id', 0), 'set X = ' , x_target, ' Y = ', y_target
    #Broadcast to the cab
    socketio.emit('new destination',{'x': x_target, 'y': y_target }, namespace='/cab')
    
 

#
# The cab SocketIO
#

#the first cab's connection
@socketio.on('connect', namespace='/cab')
def client_connect():
    global nb_of_cab    
    session['id'] = nb_of_cab 
    print('Cab connected, ID : ' + str(nb_of_cab))    
    nb_of_cab+=1
 
    
#the end of sio deconnection
@socketio.on('disconnect', namespace='/cab')
def client_disconnect():
    global nb_of_cab
    nb_of_cab-=1
    print('Cab disconnected, ID : ' + str(session.get('id', 0)))


#the cab agrees to retrieve client
@socketio.on('cab ok', namespace='/client')
def client_set_new_target(message):
    cab_id = session.get('id', 0)
    x_target = message['x']
    y_target = message['y']
    print 'New target, cab with ID :', cab_id, 'set X = ' , x_target, ' Y = ', y_target
    map.set_cab_state(cab_id, False, True, +1, x_target, y_target )
    #set the distance since the last course to 0
    map.set_cab_travelled(cab_id, 0, 0)
    #Broadcast than that the map changed for all clients
    emit('new map is available', broadcast=True)
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
