from functions import is_power_of_two, get_digits
import random

class Game:

    # Initialisations
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        
        for y in range(4):
            row = []
            for x in range(4):
                row.append(" ")
            
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
                if self.get_tile(x, y) == " ":
                    empty.append((x, y))

        return empty

    # Interact With Board
    def place_tile(self, tile, x, y):
        if x < 0 or x > 3 or y < 0 or y > 3:
            raise ValueError(f"Index out of bounds: {x} {y}")
        elif tile != " " and not isinstance(tile, int):
            raise TypeError(f"Tile type is invalid: {tile}")
        
        if isinstance(tile, int):
            if not is_power_of_two(tile):
                raise ValueError(f"Tile value is not a power of 2: {tile}")

        self.board[y][x] = tile
    
    def create_random_tile(self):
        empty = self.get_empty_tiles()
        
        if len(empty) == 0:
            raise ValueError(f"Cannot create a tile on a full board: \n{self}")

        rand_x, rand_y = empty[random.randint(0, len(empty)-1)]
        rand_tile = random.choice([2, 4])

        self.place_tile(rand_tile, rand_x, rand_y)
        # print(rand_position, rand_tile)

    def move(self, direction):
        if not self.can_move_down():
            print("Cannot move Down")
            return False
        
        # Go to 3rd from bottom, see if can move down
        for x in range(4):
            self.move_column(x)
        
        return True
    
    def move_column(self, x):
        y = 2
        while y >= 0:
            tile = self.get_tile(x, y)
            

            y -= 1



    def rotate_board_right(self):
        pass


    # Game Checking
    def can_move_down(self):
        # Check if can move down        
        for x in range(4):
            if self.can_move_column(x):
                return True

        return False

    def can_move_column(self, x):
        tile_exists = False
        preivous_tile = None
        for y in range(4):
            tile = self.get_tile(x, y)

            if tile_exists and tile == " ":
                return True
            elif tile == preivous_tile and tile != " ":
                return True
            elif tile != " ":
                tile_exists = True
            
            preivous_tile = tile
        
        return False

    def __repr__(self):
        display_board = ""
        
        for row in self.board:
            line = "|"
            for tile in row:
                prefix = " "*(4-get_digits(tile))
                line += prefix+ str(tile) + "|"
            display_board += line + "\n"
        
        return display_board[:-1]
        

game = Game()
game.place_tile(1024, 0, 2)
game.place_tile(2048, 0, 3)
# game.place_tile(2048, 1, 3)
print(game.can_move_down())
print(game)