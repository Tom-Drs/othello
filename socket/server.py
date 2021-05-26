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
    pass

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
        sio.emit("matchmaking", {"status": 200,
                                 "subject": "game_started",
                                 "grid": matchmaking_dict["grid"].get_grid(),
                                 "round": matchmaking_dict["grid"].get_round(),
                                 "player1": pickle.dumps(matchmaking_dict["white_player_object"]),
                                 "player2": pickle.dumps(matchmaking_dict["black_player_object"])},
                 room=matchmaking_dict["sid_white_player"])
        sio.emit("matchmaking", {"status": 200,
                                 "subject": "game_started",
                                 "grid": matchmaking_dict["grid"].get_grid(),
                                 "round": matchmaking_dict["grid"].get_round(),
                                 "player1": pickle.dumps(matchmaking_dict["black_player_object"]),
                                 "player2": pickle.dumps(matchmaking_dict["white_player_object"])},
                 room=matchmaking_dict["sid_black_player"])
        print(current_game)
    else:
        queue_matchmaking.append((sid, data["alias"]))
        sio.emit("matchmaking", {"status": 200,
                                 "subject": "wait"
                                 },
                 room=sid)


@sio.event
def put_pawn(sid, data):
    search_data = search_on_game(sid)
    if search_data:
        data_game = search_data[0]
        data_player = search_data[1]
        grid = data_game.get("grid")
        print(data_game)
        print(data_player)

        # Check if it's his round.
        if data_player == "white_player":
            color = 2
            sid_player2 = data_game.get("sid_black_player")
            if grid.get_round() % 2 == 0:
                sio.emit("put_pawn", {"status": 403,
                                      "subject": "It's not for you to play."},
                         room=sid)
                return
        else:
            sid_player2 = data_game.get("sid_white_player")
            color = 1
            if grid.get_round() % 2 != 0:
                sio.emit("put_pawn", {"status": 403,
                                      "subject": "It's not for you to play."},
                         room=sid)
                return
        print(color)
        print(grid.get_round())
        # Verify position
        if grid.player_put_pawn(data.get("position")):
            print("A pawn has played")
            print(grid.get_grid())
            black_points = calculate_points(data_game.get("black_player_object"), grid.get_grid())
            white_points = calculate_points(data_game.get("white_player_object"), grid.get_grid())
            sio.emit("update_grid", {"status": 200,
                                     "subject": "grid was updated",
                                     "grid": grid.get_grid(),
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points
                                     },
                     room=sid)
            sio.emit("update_grid", {"status": 200,
                                     "subject": "grid was updated",
                                     "grid": grid.get_grid(),
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points
                                     },
                     room=sid_player2)
        else:
            print("Player can't put")
            sio.emit("update_grid", {"status": 403,
                                     "subject": "grid can't update"},
                     room=sid)
            black_points = calculate_points(data_game.get("black_player_object"), grid.get_grid())
            white_points = calculate_points(data_game.get("white_player_object"), grid.get_grid())
        if black_points > white_points:
            black_end_message = "Vous avez gagné !"
            white_end_message = "Vous avez perdu..."
        elif white_points > black_points:
            white_end_message = "Vous avez gagné !"
            black_end_message = "Vous avez perdu..."
        else:
            black_end_message = "Il y a égalité, relancez une partie !"
            white_end_message = "Il y a égalité, relancez une partie !"

        if grid.get_round() % 2 == 0 and grid.best_move(1) is False:
            sio.emit("finish_game", {"status": 200,
                                     "subject": "game_finish",
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points,
                                     "winner": white_end_message,
                                     },
                     room=data_game.get("sid_white_player"))
            sio.emit("finish_game", {"status": 200,
                                     "subject": "game_finish",
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points,
                                     "winner": black_end_message,
                                     },
                     room=data_game.get("sid_black_player"))
            current_game.remove(search_on_game(sid)[0])
        elif grid.get_round() % 2 != 0 and grid.best_move(2) is False:
            sio.emit("finish_game", {"status": 200,
                                     "subject": "game_finish",
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points,
                                     "winner": black_end_message,
                                     },
                     room=data_game.get("sid_black_player"))
            sio.emit("finish_game", {"status": 200,
                                     "subject": "game_finish",
                                     "round": grid.get_round(),
                                     "black_player_points": black_points,
                                     "white_player_points": white_points,
                                     "winner": white_end_message,
                                     },
                     room=data_game.get("sid_white_player"))
            current_game.remove(search_on_game(sid)[0])
        print(current_game)
    else:
        sio.emit("put_pawn", {"status": 403,
                              "subject": "You aren't in a game."},
                 room=sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    search_data = search_on_game(sid)
    print(f"Queue Matchmaking {queue_matchmaking}")
    if search_data:
        data_game = search_data[0]
        data_player = search_data[1]
        if data_player == "black_player":
            sid_player2 = data_game.get("sid_white_player")
        else:
            sid_player2 = data_game.get("sid_black_player")
        sio.emit("end_game", {"status": 200,
                           "subject": "player_left",
                           },
                 room=sid_player2)
        current_game.remove(data_game)
    else:
        print("Player left matchmaking queue")
        for player in queue_matchmaking:
            if player[0] == sid:
                queue_matchmaking.remove(player)
    print("------ After delete --------")
    print(f"Queue : {queue_matchmaking}")
    print(f"Current game : {current_game}")


def search_on_game(sid):
    for game in current_game:
        if game.get("sid_black_player") == sid:
            return game, "black_player"
        elif game.get("sid_white_player") == sid:
            return game, "white_player"
    return False

def calculate_points(player_object, grid):
    return len([x for i in grid for x in i if x == player_object.get_color()])

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

# sio.emit("matchmaking", {"status": 200,
#                          "subject": "game_started",
#                          "grid": matchmaking_dict["grid"].get_grid(),
#                          "player1": matchmaking_dict["white_player_object"],
#                          "player2": matchmaking_dict["black_player_object"]},
#          room=matchmaking_dict["sid_white_player"])


