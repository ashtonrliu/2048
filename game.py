from functions import get_digits
from tile import Tile
from constants import DRUL_VALID_MOVES, WASD_VALID_MOVES
import random

class Game:
    # Initialisations
    def __init__(self):
        self.score = 0
        self.board = self.create_board()

    def create_board(self):
        board = []
        
        for y in range(4):
            row = []
            for x in range(4):
                tile = Tile()
                row.append(tile)
            
            board.append(row)
        
        return board

    # Getters
    def get_board(self):
        return self.board
    
    def get_tile(self, x, y):
        if x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f"Index out of bounds: {x} {y}")

        return self.board[y][x]

    def get_empty_tiles(self):
        empty = []
        
        for y in range(4):
            for x in range(4):
                if self.get_tile(x, y).get_value() == " ":
                    empty.append((x, y))

        return empty

    # Interact With Board
    def place_tile(self, tile_value, x, y):
        if x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f"Index out of bounds: {x} {y}")
        tile = Tile(tile_value)

        self.board[y][x] = tile
    
    def set_tile(self, tile, x, y):
        if x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f"Index out of bounds: {x} {y}")

        self.board[y][x] = tile

    def create_random_tile(self):
        empty = self.get_empty_tiles()
        
        if len(empty) == 0:
            raise ValueError(f"Cannot create a tile on a full board: \n{self}")


        rand_x, rand_y = empty[random.randint(0, len(empty)-1)]
        rand_tile_value = random.choice([2, 4])

        self.score += rand_tile_value

        self.place_tile(rand_tile_value, rand_x, rand_y)
        # print(rand_position, rand_tile)

    def move(self, direction):

        if direction == self.valid_moves[0]: # Down
            b_rotate = 0
            a_rotate = 0

        elif direction == self.valid_moves[1]: # Right
            b_rotate = 1
            a_rotate = 3
    
        elif direction == self.valid_moves[2]: # Up
            b_rotate = 2
            a_rotate = 2
        elif direction == self.valid_moves[3]: # Left
            b_rotate = 3
            a_rotate = 1

        for x in range(0, b_rotate):
            self.rotate_board_right()

        if not self.can_move_down():
            print("ERROR: Cannot move in that direction")
            for x in range(0, a_rotate):
                self.rotate_board_right()

            return False
        
        for x in range(4):
            if self.can_move_column(x):
                # Go to 3rd from bottom, see if can move down
                self.move_column(x)
        
        for x in range(0, a_rotate):
            game.rotate_board_right()

        return True
    
    def move_column(self, x):
        tile_0 = self.get_tile(x, 0) 
        tile_1 = self.get_tile(x, 1) 
        tile_2 = self.get_tile(x, 2) 
        tile_3 = self.get_tile(x, 3) 

        # Second from the bottom
        if not tile_2.is_empty():
            if tile_3.is_empty():
                # Move into empty tile
                tile_3.move_tile(tile_2)

            elif tile_3.get_value() == tile_2.get_value():
                # Addition
                tile_3.add_tile(tile_2, self)


        # Third from the bottom
        if not tile_1.is_empty():
            if tile_2.is_empty():
                # Check tile_3 which is underneath

                if tile_3.is_empty():
                    tile_3.move_tile(tile_1)
                elif tile_1.get_value() == tile_3.get_value() and not tile_3.get_merged():
                    tile_3.add_tile(tile_1, self)
                else:
                    tile_2.move_tile(tile_1)

            elif tile_1.get_value() == tile_2.get_value():
                # Addition
                tile_2.add_tile(tile_1, self)

        # Fourth from the bottom (Top)
        if not tile_0.is_empty():
            if tile_1.is_empty():
                # Check tile_2 which is underneath

                if tile_2.is_empty():
                    # Check tile_3 which is underneath
                    if tile_3.is_empty():
                        tile_3.move_tile(tile_0)
                    elif tile_0.get_value() == tile_3.get_value() and not tile_3.get_merged():
                        tile_3.add_tile(tile_0, self)
                    else:
                        tile_2.move_tile(tile_0)

                elif tile_0.get_value() == tile_2.get_value() and not tile_2.get_merged():
                    tile_2.add_tile(tile_0, self)
                else:
                    tile_1.move_tile(tile_0)
        
            elif tile_0.get_value() == tile_1.get_value():
                # Addition
                tile_1.add_tile(tile_0, self)


    def rotate_board_right(self):
        for y in range(0, 2):
            for x in range(0, 2):
                origin = [x, y]
                o_tile = self.get_tile(origin[0], origin[1])

                for num in range(0, 4):
                    dest = [3 - origin[1] , origin[0]]
                    # print(dest)
                    save_tile = self.get_tile(dest[0], dest[1])
                    self.set_tile(o_tile, dest[0], dest[1])

                    origin = dest
                    o_tile = save_tile


                # (0, 0) --> (3, 0) --> (3, 3) --> (0, 3) --> (0, 0)
                # (1, 0) --> (3, 1) --> (2, 3) --> (0, 2) --> (1, 0)
                # (0, 1) --> (2, 0) --> (3, 2) --> (1, 3) --> (0, 1)
                # (1, 1) --> (2, 1) --> (2, 2) --> (1, 2) --> (1, 1)
                # Algorithm:
                # x --> length - y
                # y --> x

    # Game Checking
    def can_move_down(self):
        # Check if can move down        
        for x in range(4):
            if self.can_move_column(x):
                return True

        return False

    def can_move_column(self, x):
        tile_exists = False
        preivous_tile_value = None
        for y in range(4):
            tile = self.get_tile(x, y)
            tile_value = tile.get_value()

            if tile_exists and tile_value == " ":
                return True
            elif tile_value == preivous_tile_value and tile_value != " ":
                return True
            elif tile_value != " ":
                tile_exists = True
            
            preivous_tile_value = tile_value
        
        return False

    def can_continue(self):
        # Check down
        d = self.can_move_down()
        self.rotate_board_right()
        r = self.can_move_down()
        self.rotate_board_right()
        u = self.can_move_down()
        self.rotate_board_right()
        l = self.can_move_down()
        self.rotate_board_right()

        return d or r or u or l

    def reset_merged(self):
        for y in range(0, 4):
            for x in range(0, 4):
                self.get_tile(x, y).reset_merged()

    def __repr__(self):
        print(f"SCORE: {self.score}")

        display_board = ""
        
        for row in self.board:
            line = "|"
            for tile in row:
                prefix = " "*(4-get_digits(tile))
                line += prefix+ str(tile) + "|"
            display_board += line + "\n"
        
        return display_board[:-1]

    def choose_moveset(self):
        print("Welcome to 2048, Choose controls by typing '1' or '2': ")
        print("\t1. WASD")
        print("\t2. DRUL")
        
        while True:
            controls = input("$ ")
            if controls == "1":
                self.valid_moves = WASD_VALID_MOVES
                return
            elif controls == "2":
                self.valid_moves = DRUL_VALID_MOVES
                return
            else:
                print("ERROR: Invalid control type, enter '1' or '2'")
    
    def game_finish(self):
        print("Game Over!")
        print("Final board: ")
        print(self)
        exit(0)

    def run_game(self):
        # Create two random tiles
        
        self.choose_moveset()
        
        self.create_random_tile()
        self.create_random_tile()

        while True:
            print(self)

            move = input("Enter move : $ ").upper()

            if move == "EXIT":
                self.game_finish()

            elif move not in self.valid_moves:
                print("ERROR: Direction not recognised")
            
            elif self.move(move):
                self.reset_merged()
                self.create_random_tile()

                if not self.can_continue():
                    self.game_finish()

if __name__ == "__main__":
    game = Game()
    game.run_game()