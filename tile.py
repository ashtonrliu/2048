from functions import is_power_of_two

class Tile:

    # Initialisations
    def __init__(self, value = " "):
        self.set_value(value)

        self.merged = False

    def set_value(self, value):
        if value != " " and not isinstance(value, int):
            raise TypeError(f"Tile value is invalid: {value}, {type(value)}")
        
        if isinstance(value, int):
            if not is_power_of_two(value):
                raise ValueError(f"Tile value is not a power of 2: {value}")
    
        self.value = value
    
    def add_tile(self, tile, game):
        # self is the one being added to value becomes current + other
        # tile gets cleared
        self.set_value(self.get_value() + tile.get_value())
        game.score += self.get_value()
        self.set_merged()

        tile.set_value(" ")

    def move_tile(self, tile):
        # Self has their " " value updated to the tile value
        self.set_value(tile.get_value())
        tile.set_value(" ")
        

    def is_empty(self):
        return self.value == " "

    def get_value(self):
        return self.value
    
    def get_merged(self):
        return self.merged

    def set_merged(self):
        self.merged = True
    
    def reset_merged(self):
        self.merged = False

    def __repr__(self):
        return str(self.value)