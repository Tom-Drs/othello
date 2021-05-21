import eventlet
import socketio
import random
import pickle
import game

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

queue_matchmaking = []

current_game = []


@sio.event
def connect(sid, environ):
    print("A player join Othello server !")


# @sio.event
# def matchmaking(sid, data):
#     print('Player want to play at othello !')
#     if len(queue_matchmaking) >= 1:
#         current_game["black_player"] = sid
#         current_game["white_player"] = queue_matchmaking[0]
#         current_game["grid"] = "game started"
#         sio.emit('matchmaking', "The game started", room=sid)
#         sio.emit('matchmaking', "The game started", room=current_game["white_player"])
#         queue_matchmaking.remove(current_game["white_player"])
#         print("We have 2 players, I can start the game !")
#         print(current_game)
#     else:
#         queue_matchmaking.append(sid)
#         sio.emit('matchmaking', "Waiting for start the game", room=sid)


@sio.event
def matchmaking(sid, data):
    print("Player join queue")
    if len(queue_matchmaking) >= 1:
        if random.randint(0, 1) == 0:
            player1 = (sid, data["alias"])
            player2 = queue_matchmaking[0]
        else:
            player1 = queue_matchmaking[0]
            player2 = (sid, data["alias"])
        matchmaking_dict = {
            "sid_black_player": player1[0],
            "sid_white_player": player2[0],
            "black_player_object": game.Player(1),
            "white_player_object": game.Player(2),
            "grid": game.Grid(),
        }
        matchmaking_dict["black_player_object"].edit_alias(player1[1])
        matchmaking_dict["white_player_object"].edit_alias(player2[1])
        current_game.append(matchmaking_dict)

        queue_matchmaking.remove(queue_matchmaking[0])
        print("here")
        sio.emit("matchmaking", {"response": {"status": 200,
                                              "subject": "game_started",
                                              "grid": matchmaking_dict["grid"].get_grid(),
                                              "player1": pickle.dumps(matchmaking_dict["white_player_object"]),
                                              "player2": pickle.dumps(matchmaking_dict["black_player_object"])},},
                 room=matchmaking_dict["sid_white_player"])
        print("here")
        sio.emit("matchmaking", {"response": {"status": 200,
                                              "subject": "game_started",
                                              "grid": matchmaking_dict["grid"].get_grid(),
                                              "player1": pickle.dumps(matchmaking_dict["black_player_object"]),
                                              "player2": pickle.dumps(matchmaking_dict["white_player_object"])},},
                 room=matchmaking_dict["sid_black_player"])
        matchmaking_dict = 0
        print(current_game)
    else:
        queue_matchmaking.append((sid, data["alias"]))
        sio.emit("matchmaking", {
            "status": 200,
            "subject": "wait"
        }, room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

# sio.emit("matchmaking", {"status": 200,
#                          "subject": "game_started",
#                          "grid": matchmaking_dict["grid"].get_grid(),
#                          "player1": matchmaking_dict["white_player_object"],
#                          "player2": matchmaking_dict["black_player_object"]},
#          room=matchmaking_dict["sid_white_player"])

