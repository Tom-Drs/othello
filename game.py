from tkinter import *
from tkinter.ttk import *

class Player:
    """Class for create a player.
        Args:
            color (int): color of the player.
    """

    def __init__(self, color):
        self.color = color
        self.points = 0

    def calculate_points(self, grid):
        """Class method for calculating all player points"""
        self.points = len([x for i in grid for x in i if x == self.color])
        return self.points

class Grid:
    """Class for create a othello grid.
    """

    def __init__(self):
        self.grid = [[0 for i in range(8)] for i in range(8)]
        self.first_pawns()
        self.round = 0

    def first_pawns(self):
        """Class method for put init 4 pawns on the grid.
        """
        self.put_pawn((3, 3), 2)
        self.put_pawn((3, 4), 1)
        self.put_pawn((4, 3), 1)
        self.put_pawn((4, 4), 2)

    def put_pawn(self, position, color):
        """Class method for put a pawn on the grid.
            Args:
                position (tuple) : Square position.
                color (int) : Color of the pawn.
        """
        self.grid[position[0]][position[1]] = color


    def print_grid(self):
        """Class method for print the grid.
        """
        for i in self.grid:
            print(i)

    def diagonals_lines_of_pawn(self, position):
        first_pos_left = (0, position[1] - position[0])  # Get position of diagonal on the line 0
        first_pos_right = (0, position[1] + position[0])  # Get position of diagonal on the line 0
        vertical_line = [(i, position[1], self.grid[i][position[1]]) for i in range(8)]  # Get the vertical line
        horizontal_line = [(position[0], i, self.grid[position[0]][i]) for i in range(8)]  # Get de horizontal line
        diagonal_left = []
        diagonal_right = []
        # Get all pawn's position on the diagonal left
        for i in range(8):
            if first_pos_left[1] + i < 0 or first_pos_left[1] + i > 7:
                continue
            diagonal_left.append((i, first_pos_left[1] + i, self.color((i, first_pos_left[1] + i))))
        # Get all pawn's position on the diagonal right
        for i in range(8):
            if first_pos_right[1] - i < 0 or first_pos_right[1] - i > 7:
                continue
            diagonal_right.append((i, first_pos_right[1] - i, self.color((i, first_pos_right[1] - i))))

        diagonals_lines = {
            "horizontal_line": tuple(horizontal_line),
            "vertical_line": tuple(vertical_line),
            "diagonal_left": tuple(diagonal_left),
            "diagonal_right": tuple(diagonal_right)
        }
        return diagonals_lines

    def color(self, position):
        return self.grid[position[0]][position[1]]

    def near(self, position):
        """Class method for get all pawns near a position.
            Args:
                position (tuple): Square position.
            Returns:
                dict of all pawns near.
        """

        near_list = []
        if position[0] - 1 < 0:
            near_list.append(None)
        else:
            near_list.append((position[0] - 1, position[1], self.grid[position[0] - 1][position[1]]))
        if position[0] + 1 > 7:
            near_list.append(None)
        else:
            near_list.append((position[0] + 1, position[1], self.grid[position[0] + 1][position[1]]))
        if position[1] - 1 < 0:
            near_list.append(None)
        else:
            near_list.append((position[0], position[1] - 1, self.grid[position[0]][position[1] - 1]))
        if position[1] + 1 > 7:
            near_list.append(None)
        else:
            near_list.append((position[0], position[1] + 1, self.grid[position[0]][position[1] + 1]))
        if position[0] - 1 < 0 or position[1] - 1 < 0:
            near_list.append(None)
        else:
            near_list.append((position[0] - 1, position[1] - 1, self.grid[position[0] - 1][position[1] - 1]))
        if position[0] + 1 > 7 or position[1] + 1 > 7:
            near_list.append(None)
        else:
            near_list.append((position[0] + 1, position[1] + 1, self.grid[position[0] + 1][position[1] + 1]))
        if position[0] - 1 < 0 or position[1] + 1 > 7:
            near_list.append(None)
        else:
            near_list.append((position[0] - 1, position[1] + 1, self.grid[position[0] - 1][position[1] + 1]))
        if position[0] + 1 > 7 or position[1] - 1 < 0:
            near_list.append(None)
        else:
            near_list.append((position[0] + 1, position[1] - 1, self.grid[position[0] + 1][position[1] - 1]))

        near_dict = {
            "top": near_list[0],
            "bottom": near_list[1],
            "left": near_list[2],
            "right": near_list[3],
            "diagonal_left_top": near_list[4],
            "diagonal_right_bot": near_list[5],
            "diagonal_right_top": near_list[6],
            "diagonal_left_bot": near_list[7]
        }
        return near_dict

    def can_put(self, position, color):
        """Class method for return list of pawn's combination on the different axes.
            Args:
                position (tuple): Square position.
                color (int): Color of the pawn.
            Return:
                tuple of pawn's combination on the different axes.
        """
        pawns_convert = []
        for key, value in self.near(position).items():
            # print(position, key, value)
            if value is None or color == value[2] or value[2] == 0:
                continue
            elif self.grid[position[0]][position[1]] != 0:
                break
            else:
                if key == "bottom":
                    pawns_add = self.calculate_pawn_list("vertical_line", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "top":
                    pawns_add = self.calculate_pawn_list_backward("vertical_line", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "right":
                    pawns_add = self.calculate_pawn_list("horizontal_line", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "left":
                    pawns_add = self.calculate_pawn_list_backward("horizontal_line", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "diagonal_right_bot":
                    pawns_add = self.calculate_pawn_list("diagonal_left", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "diagonal_left_top":
                    pawns_add = self.calculate_pawn_list_backward("diagonal_left", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "diagonal_left_bot":
                    pawns_add = self.calculate_pawn_list("diagonal_right", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)

                elif key == "diagonal_right_top":
                    pawns_add = self.calculate_pawn_list_backward("diagonal_right", position, color)
                    if pawns_add is not None:
                        for pawn in pawns_add:
                            pawns_convert.append(pawn)
        # print(position)
        # print(pawns_convert)
        return tuple(pawns_convert)

    def calculate_pawn_list(self, line, position, color):
        """"Class method for finding the pawns to return in a list.
            Args:
                line (str): line for find pawns (diagonal / horizontal / vertical) - (right / bot)
                position (tuple): position of the initial pawn.
                color (int): color of the initial pawn.
            Returns:
                None: if there aren't pawn to flip.
                list: pawn list to flip.
        """
        pawns_add = []
        index_next_pawns = self.diagonals_lines_of_pawn(position).get(line)
        list_pawns = self.diagonals_lines_of_pawn(position).get(line)
        # print(position[0], position[1], color)
        index_next_pawns = index_next_pawns.index((position[0], position[1], 0))
        for pawn in list_pawns[index_next_pawns + 1:]:
            if pawn[2] != color and pawn[2] != 0:
                pawns_add.append(pawn)
            elif pawn[2] == color:
                return pawns_add
            elif pawn[2] == 0:
                return None

    def calculate_pawn_list_backward(self, line, position, color):
        """"Class method for finding the pawns to return in a backward list.

            Args:
                line (str): line for find pawns (diagonal / horizontal / vertical) - (right / bot)
                position (tuple): position of the initial pawn.
                color (int): color of the initial pawn.
            Returns:
                None: if there aren't pawn to flip.
                list: pawn list to flip.
        """
        pawns_add = []
        index_next_pawns = self.diagonals_lines_of_pawn(position).get(line)
        list_pawns = self.diagonals_lines_of_pawn(position).get(line)
        # print(position[0], position[1], color)
        index_next_pawns = index_next_pawns.index((position[0], position[1], 0))
        list_pawns = list_pawns[:index_next_pawns]
        for pawn in range(len(list_pawns)-1, -1, -1):
            if list_pawns[pawn][2] != color and list_pawns[pawn][2] != 0:
                pawns_add.append(list_pawns[pawn])
            elif list_pawns[pawn][2] == color:
                return pawns_add
            elif list_pawns[pawn][2] == 0:
                return None

    def player_put_pawn(self, position):
        """Class method for a player to place a pawn and flips all pawn's combination.

            Args:
                position (tuple): position of the pawn.
                color (int): color of the pawn.
            Returns:
                None: if the pawn cannot be placed.
.               True: if the pawn has been placed.
        """
        if self.round % 2 == 0:
          color = 1
        else:
          color = 2
        combination = self.can_put(position, color)
        if len(combination) == 0:
            return None
        if len(combination) > 0:
            self.put_pawn(position, color)
            for i in combination:
                self.put_pawn((i[0], i[1]), color)
        self.add_round()
        return True

    def best_move(self, color):
        """Class method for return the best move.
            Args:
                color(int): color of the pawn.
            Returns:
                None: if there isn't any best move.
                tuple: (number of pawns that the move will return) and (position of the best move).
        """
        best_move_pawns = 0
        best_move_pos = 0
        for row in range(7):
            for column in range(7):
                if len(self.can_put((row, column), color)) > best_move_pawns:
                    best_move_pos = (row, column, color)
                    best_move_pawns = len(self.can_put((row, column), color))
        if best_move_pawns == 0:
            return None
        return best_move_pawns, best_move_pos
    
    def add_round(self):
        """Class method to add a round.
            Return:
                int: number of round
        """
        self.round += 1
        return self.round

    def round(self):
        return self.round

    def grid(self):
        return self.grid


