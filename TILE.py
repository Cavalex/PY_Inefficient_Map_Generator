import random

# the terrains will be in the form Type : Rarity,
# the oceans will be filled differently so I'll put a 0 in there
normal_terrains = {
    "Swamp": 1,
    "Desert": 1,
    "Grassland": 2,
    "Plains": 2,
    "Prairie": 2,
    "Steppe": 1,
}

resources = {
        "Fish":3,
        "Clam":2,
        "Whale":2,
        "Horses":2, # Bonus in Warfare
        "Ivory":2, # Bonus in Warfare
        "Fruits":2,
        "Dyes":2,
        "Sugar":2,
        "Pasture":2,
        "Wheat":3,
        "Corn":2,
        "Rice":2,
        "Game":2,
        "Furs":2,
        "Silk":2,
        "Spices":2,
        "Woods":2, # Bonus in Naval and Defensive Warfare
        "Wine":2,
        "Iron":2, # Very important in Warfare
        "Gold":3,
        "Gems":3,
        "Silver":2,
        "Copper":1, # Substitute for iron
        "Stone":2, # Bonus in Defensive Warfare
        "Marble":2 # Bonus in Defensive Warfare
        }

class Tile:

    def __init__(self, map, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.height_value = None
        self.map = map
        self.terrain = None
        self.resource = []
        self.forest = None
        self.hill = None
        self.huge_hill = None
        self.value_wealth = None
        self.value_production = None
        self.value_food = None
        self.population = None
        self.owner = None
        self.elevation = None # between 0 and 3
        self.troops = []
        self.buildings = [] # the city will be in here

    def get_neighbours(self):
        neighbours = []
        # the neighbours will be all 4 adjacent tiles so:
        neighbour1_pos = [self.x + 1, self.y + 0]
        neighbour2_pos = [self.x + 0, self.y + 1]
        neighbour3_pos = [self.x - 1, self.y + 0]
        neighbour4_pos = [self.x + 0, self.y - 1]
        neighbours_pos = [neighbour1_pos, neighbour2_pos, neighbour3_pos, neighbour4_pos]
        for n in neighbours_pos:
            if n[0] < self.map.width and n[1] < self.map.height:
                for t in self.map.tiles:
                    if t.x == n[0] and t.y == n[1]:
                        neighbours.append(t)
        return neighbours
