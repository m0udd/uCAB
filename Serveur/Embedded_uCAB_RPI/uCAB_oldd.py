from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask.ext.socketio import SocketIO
from flask.ext.socketio import close_room
from flask.ext.socketio import disconnect
from flask.ext.socketio import emit
from flask.ext.socketio import join_room
from flask.ext.socketio import leave_room
import json
from threading import Thread
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pass'
socketio = SocketIO(app)
thread = None

map = [
{
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
                ]
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
                ]
            }
        }
    ]
}]

json_str = json.dumps(map, ensure_ascii=False )
map = json.loads(json_str)

def json_to_str_map():
    return json.dumps(map, ensure_ascii=False )

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(5)
        count += 1
        socketio.emit('my response',
                      {'data': 'background_thread', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
         'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
         'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
    
# My CODE here -----------------------------------------------------------------
global nb_of_client
nb_of_client = 0

@socketio.on('connect', namespace='/client')
def client_connect():
    global nb_of_client
    nb_of_client+=1
    session['id'] = nb_of_client
    print('Client connected, ID : ' + str(nb_of_client))
    #emit('my response', {'data': 'Connected', 'id': nb_of_client})


@socketio.on('disconnect', namespace='/client')
def client_disconnect():
    global nb_of_client
    nb_of_client-=1
    print('Client disconnected, ID : ' + str(session.get('id', 0)))

    
@socketio.on('get map', namespace='/client')
def client_get_map():
    if nb_of_client == 3:     
        emit('new map', map[0]['areas'][0])
    else:
        emit('no map', {'data': "The server have not 3 clients ! sorry... :( "})
    
@socketio.on('new target', namespace='/client')
def client_get_new_target(message):
    x_target = message['x']
    y_target = message['y']
    print('New target, clinet with ID : ', str(session.get('id', 0)) 
    + " set X = " , x_target + ", Y = " , y_target )

# My CODE here -----------------------------------------------------------------

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
