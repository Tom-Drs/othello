from tkinter import *

import game
import time

class BtnGridUi:
    def __init__(self, x, y, image, grid_ui, grid_game):
        self.grid_ui = grid_ui
        self.grid_game = grid_game
        self.white_photo = PhotoImage(file=r"pion_blanc.pgm")
        self.black_photo = PhotoImage(file=r"pion_noir.pgm")
        self.x = x
        self.y = y
        self.btn = Button(self.grid_ui.window, image=image, command=self.click_ui).grid(row=self.x, column=self.y)

    def click_ui(self):
        if self.grid_ui.player_put_pawn((self.x, self.y)):
            # self.btn.destroy()
            if self.grid_game.color((self.x, self.y)) == 1:
                self.btn = BtnGridUi(self.x, self.y, self.black_photo, self.grid_ui, self.grid_game)
            else:
                self.btn = BtnGridUi(self.x, self.y, self.white_photo, self.grid_ui, self.grid_game)

            if self.grid_ui.bot and self.grid_game.round() % 2 != 0:
                # print(super().best_move(2))
                self.grid_ui.player_put_pawn(self.grid_game.best_move(2)[1])

class OthelloUi(game.Grid):

    def __init__(self):

        self.window = Tk()
        self.window.title("Othello")
        self.window.geometry("400x400")

        self.grid_photo = PhotoImage(file = r"grille.pgm")
        self.white_photo = PhotoImage(file = r"pion_blanc.pgm")
        self.black_photo = PhotoImage(file = r"pion_noir.pgm")
        self.bot = False

        Button(self.window, text="Deux Joueurs", command=self.add_player_ui).grid(row=4, column=5, pady=100, padx=150)
        Button(self.window, text="Contre Ordinateur", command=self.against_bot).grid(row=5, column=5)

        self.window.mainloop()

    def grid_ui(self):
        for x in range (8):
            for y in range (8):
                BtnGridUi(x, y, self.grid_photo, self, super())
        BtnGridUi(3, 3, self.white_photo, self, super())
        BtnGridUi(3, 4, self.black_photo, self, super())
        BtnGridUi(4, 3, self.black_photo, self, super())
        BtnGridUi(4, 4, self.white_photo, self, super())


    def destroy_ui(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def add_player_ui(self):
        self.destroy_ui()

        self.name_player_1 = StringVar()
        self.name_player_1.set("Joueur 1")
        Entry(self.window, textvariable=self.name_player_1, width=15).grid(row=4, column=5, pady=50, padx=150)

        self.name_player_2 = StringVar()
        self.name_player_2.set("Joueur 2")
        Entry(self.window, textvariable=self.name_player_2, width=15).grid(row=6, column=5, pady=50)

        Button(self.window, text="Valider", command=self.game_players).grid(row=5, column=5, pady=25)

        self.black_player = game.Player(1)
        self.white_player = game.Player(2)

    def game_players(self):
        super().__init__()
        if self.bot:
            self.player_1 = "Vous"
            self.player_2 = "Bot"
            self.black_player = game.Player(1)
            self.white_player = game.Player(2)
        else:
            self.player_1 = self.name_player_1.get()
            self.player_2 = self.name_player_2.get()

        self.destroy_ui()
        self.grid_ui()


        Label(self.window, text=self.player_1).grid(row=4, column=10)
        Label(self.window, text=self.player_2).grid(row=5, column=10)
        Label(self.window, image=self.black_photo).grid(row=4, column=9)
        Label(self.window, image=self.white_photo).grid(row=5, column=9)

        Label(self.window, text="Autour de: ").grid(row=0, column=9)
        self.round_ui(self.black_photo)
        self.point_player_1 = StringVar()
        self.point_player_1.set("0")
        Label(self.window, textvariable=self.point_player_1).grid(row=4, column=8)
        self.point_player_2 = StringVar()
        self.point_player_2.set("0")
        Label(self.window, textvariable=self.point_player_2).grid(row=5, column=8)

        Button(self.window, text="Quitter", command=self.window.quit).grid(row=9, column=8, columnspan=3)

    def against_bot(self):
        self.bot = True
        self.game_players()

    def calculate_point_ui(self):
        self.point_player_1.set(self.black_player.calculate_points(super().grid()))
        self.point_player_2.set(self.white_player.calculate_points(super().grid()))

    def round_ui(self, image):
        Label(self.window, image=image).grid(row=0, column=10)

    def end_game_ui(self):
        round = len([x for i in super().grid() for x in i if x == 1]) + len(
            [x for i in super().grid() for x in i if x == 2])
        if round % 2 == 0:
            last_pawn = super().best_move(1)
        else:
            last_pawn = super().best_move(2)

        if last_pawn is None:
            self.destroy_ui()
            if self.black_player.calculate_points(super().grid()) < self.white_player.calculate_points(super().grid()):
                Label(self.window, text=self.point_player_2.get()).grid()
                Label(self.window, text=self.player_2).grid()
            else:
                Label(self.window, text=self.point_player_1.get()).grid()
                Label(self.window, text=self.player_1).grid()

    def player_put_pawn(self, position):
        """Class method for a player to place a pawn and flips all pawn's combination.

            Args:
                position (tuple): position of the pawn.
                color (int): color of the pawn.
            Returns:
                False: if the pawn cannot be placed.
.               True: if the pawn has been placed.
        """
        if super().round() % 2 == 0:
            color = 1
        else:
            color = 2
        combination = super().can_put(position, color)
        if len(combination) == 0:
            return False
        if len(combination) > 0:
            self.put_pawn_ui(position, color)
            for i in combination:
                self.put_pawn_ui((i[0], i[1]), color)
        super().add_round()
        self.calculate_point_ui()
        self.end_game_ui()
        return True

    def put_pawn_ui(self, position, color):
        super().put_pawn(position, color)
        if color == 1:
          self.round_ui(self.white_photo)
          BtnGridUi(position[0], position[1], self.black_photo, self, super())
        else:
          BtnGridUi(position[0], position[1], self.white_photo, self, super())
          self.round_ui(self.black_photo)




