import othello
import random

def main():
    bot = othello.Player(2)
    player = othello.Player(1)
    grid = othello.Grid()
    while True:
        print("C'est à vous de jouer (vous êtes noir).")
        print("--------------------------------------")
        grid.print_grid()
        if grid.best_move() is not None:
            pos = input("Entrez une position pour poser un pion. ( (int(ligne) + int(colonne) exemple : 00 ) :")
            while grid.player_put_pawn((int(pos[0]), int(pos[1]))) is None:
                print("Position rentrée incorrecte.")
                pos = input("Entrez une position pour poser un pion.")
            print(f"Vos points : {player.calculate_points(grid)} \nPoints du bot : {bot.calculate_points(grid)}.")
        else:
            print("La partie est terminé !")
            print(f"Vos points : {player.calculate_points(grid)} \nPoints du bot : {bot.calculate_points(grid)}.")
            return
        print("--------------------------------------")
        print("Le bot est en train de jouer...")
        if grid.best_move() is not None:
            move = grid.best_move()
            grid.player_put_pawn((move[1][0], move[1][1]))
            print(f"Le bot a posé son pion en {move[1][0], move[1][1]}.")
            print(f"Vos points : {player.calculate_points(grid)} \nPoints du bot : {bot.calculate_points(grid)}.")
        else:
            print("La partie est terminé !")
            print(f"Vos points : {player.calculate_points(grid)} \nPoints du bot : {bot.calculate_points(grid)}.")
            return

if __name__ == "__main__":
    main()