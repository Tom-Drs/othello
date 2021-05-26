import socketio
import pickle
from tkinter import *
import sys, os

sio = socketio.Client()
ui2 = 0
@sio.event
def connect():
    print('connection established')


@sio.event
def matchmaking(data):
    global ui
    if data.get("subject") == "wait":
        print(data)
        # player_object = pickle.loads(data.get("player1"))
        # print(data)
        # print(player_object.get_alias())
        # sio.emit("put_pawn", {"status": 200,
        #                       "subject": "Want put pawn.",
        #                       "position": (2, 3)})
    elif data.get("subject") == "game_started":
        print(data.get("grid"))
        ui2.game_start(data)
        ui2.update_ui(data.get("grid"), data.get("round"), data.get("white_player_points"), data.get("black_player_points"))



@sio.event
def disconnect():
    print('disconnected from server')

@sio.event
def end_game(data):
    if data.get("subject") == "player_left":
        ui2.main_menu()


@sio.event
def put_pawn(data):
    print(data)

@sio.event
def update_grid(data):
    ui2.update_ui(data.get("grid"), data.get("round"), data.get("white_player_points"), data.get("black_player_points"))

@sio.event
def finish_game(data):
    print(data)
    ui2.end_dashboard(data)


class BtnGridUi:
    def __init__(self, x, y, image):
        self.grid_ui = ui2
        self.x = x
        self.y = y
        self.btn = Button(self.grid_ui.window, image=image, command=self.click_ui).grid(row=self.x, column=self.y)

    def click_ui(self):
        sio.emit("put_pawn", {"position": (self.x, self.y)})

class OthelloUi:

    def __init__(self):
        global ui2
        self.window = Tk()
        self.window.title("Othello")
        self.window.geometry("400x400")
        ui2 = self
        self.grid_photo = PhotoImage(file=get_path("grille.pgm"))
        self.white_photo = PhotoImage(file=get_path("pion_blanc.pgm"))
        self.black_photo = PhotoImage(file=get_path("pion_noir.pgm"))
        self.main_menu()
        self.window.mainloop()


    # def grid_ui(self):
    #     for x in range (8):
    #         for y in range (8):
    #             BtnGridUi(x, y, self.grid_photo, self, super())
    #     BtnGridUi(3, 3, self.white_photo, self, super())
    #     BtnGridUi(3, 4, self.black_photo, self, super())
    #     BtnGridUi(4, 3, self.black_photo, self, super())
    #     BtnGridUi(4, 4, self.white_photo, self, super())

    def destroy_ui(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def launch_matchmaking(self):
        sio.emit('matchmaking', {
            "alias": self.name_player.get(),
        })
        self.destroy_ui()
        Label(self.window, text="Veuillez patienter, nous recherchons un adversaire").pack()

    def update_ui(self, grid, round, white_points, black_points):
        for x in range(8):
            for y in range(8):
                if grid[x][y] == 0:
                    BtnGridUi(x, y, self.grid_photo)
                elif grid[x][y] == 1:
                    BtnGridUi(x, y, self.black_photo)
                elif grid[x][y] == 2:
                    BtnGridUi(x, y, self.white_photo)

        Label(self.window, text="Autour de: ").grid(row=0, column=9)
        if round % 2 == 0:
            Label(self.window, image=self.black_photo).grid(row=0, column=10)
        else:
            Label(self.window, image=self.white_photo).grid(row=0, column=10)
        self.black_points.set(black_points)
        self.white_points.set(white_points)

    def game_start(self, data):
        self.destroy_ui()
        player1 = pickle.loads(data.get("player1"))
        player2 = pickle.loads(data.get("player2"))

        Label(self.window, text=player1.get_alias()).grid(row=4, column=10)
        Label(self.window, text=player2.get_alias()).grid(row=5, column=10)
        self.white_points = StringVar()
        self.white_points.set("2")
        self.black_points = StringVar()
        self.black_points.set("2")
        print(self.black_points)

        if player1.get_color() == 1:
            Label(self.window, image=self.black_photo).grid(row=4, column=9)
            Label(self.window, image=self.white_photo).grid(row=5, column=9)

            Label(self.window, textvariable=self.black_points).grid(row=4, column=8)
            Label(self.window, textvariable=self.white_points).grid(row=5, column=8)
        else:
            Label(self.window, image=self.white_photo).grid(row=4, column=9)
            Label(self.window, image=self.black_photo).grid(row=5, column=9)

            Label(self.window, textvariable=self.black_points).grid(row=5, column=8)
            Label(self.window, textvariable=self.white_points).grid(row=4, column=8)



    def main_menu(self):
        self.destroy_ui()
        self.name_player = StringVar()
        self.name_player.set("Votre pseudo")
        Entry(self.window, textvariable=self.name_player, width=15).grid(row=4, column=5, pady=50, padx=150)
        Button(self.window, text="Rechercher une partie", command=self.launch_matchmaking).grid(row=5, column=5)

    def end_dashboard(self, data):
        self.destroy_ui()
        self.end = StringVar()
        self.end.set(data.get("winner"))
        self.destroy_ui()
        Label(self.window, textvariable=self.end).pack()
        Button(self.window, text="Menu", command=self.main_menu).pack()



def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    sio.connect('http://othello.tomyserver.fr:5000')
    ui = OthelloUi()



