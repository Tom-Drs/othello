import socketio
import pickle
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('matchmaking', {
        "alias": "Tomy",
    })

@sio.event
def matchmaking(data):
    if data.get("subject") == "wait":
        print(data)
    else:
        player_object = pickle.loads(data["response"]["player1"])
        print(data)
        print(player_object.get_alias())
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
