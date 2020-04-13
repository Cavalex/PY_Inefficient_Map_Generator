from tkinter import *
import random
from TILE import Tile

terrains = ["Swamp", "Desert", "Grassland", "Plains", "Prairie", "Steppe"]
normal_terrains = ["Grassland", "Plains", "Prairie"]

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.number_of_tiles = width * height
        self.tiles = []

    def fill_tiles(self):
        self.idCounter = 1
        for x in range(self.height):
            for y in range(self.width):
                newTile = Tile(self, self.idCounter, x, y)
                self.tiles.append(newTile)
                self.idCounter += 1

        random_tile = random.choice(self.tiles)
        max_value = 200
        random_tile.height_value = random.randint(1, max_value)
        _height = random_tile.height_value
        r = random.randint(5, 15)
        y = random.randint(1, 10)
        break_loop = False

        l = 0
        # I really have to get a better algorithm
        while not break_loop:
            # 100 will create big clusters while 1 will create small ones
            _height -= r
            neighbours = random_tile.get_neighbours()
            for n in neighbours:
                n.terrain = random_tile.terrain
                if _height > max_value / 2:
                    for n2 in n.get_neighbours():
                        n2.terrain = random_tile.terrain
                    _height = max_value / 2 ###

            if _height <= 0:
                if y == 1 or y == 2 or y == 3:
                    random_tile.terrain = random.choice(terrains)
                elif y == 10:
                    random_tile.terrain = "Ocean"
                else:
                    random_tile.terrain = random.choice(normal_terrains)
                #print(l)
                #print("{}: ({}, {}) --> {}".format(random_tile.id, random_tile.x, random_tile.y, random_tile.terrain))
                for t in self.tiles:
                    if t.terrain is None:
                        break_loop = False
                        break
                    else:
                        break_loop = True
                    if random_tile.id == t.id:
                        t = random_tile
                        t.height_value = random_tile.height_value
                        print(t.height_value)
                random_tile = random.choice(self.tiles)
                random_tile.height_value = random.randint(1, 200)
                _height = random_tile.height_value
                r = random.randint(5, 15)
                y = random.randint(1, 10)
                l += 1

        self.clean_map()
        self.clean_map()
        self.clean_map()
        for tile in self.tiles:
            self.fill_resources(tile)
            self.generate_hills(tile)
            self.generate_forest(tile)
            self.generate_population(tile)
            self.generate_value(tile)

    # Cleaning the map with another algorithm
    def clean_map(self):
        for t in self.tiles:
            biome = ""
            l = 0
            for n in t.get_neighbours():
                if l == 0:
                    biome = n.terrain
                    l = 1
                if n.terrain == biome:
                    continue
                else:
                    biome = "not changing"
            if biome != "not changing":
                t.terrain = biome

    def fill_resources(self, t):
        roll = 2
        while roll > 0:
            if t.terrain == "Ocean":
                chance = 34  # 1 in 3 ts contain resources
                resources = ["Whale"] * 1 + ["Fish"] * 8
            elif t.terrain == "Swamp":
                chance = 5
                resources = ["Copper"] * 2 + ["Iron"] * 1
            elif t.terrain == "Desert":
                chance = 10
                resources = ["Copper"] * 5 + ["Marble"] * 3 + ["Gems"] * 1
            elif t.terrain == "Steppe":
                chance = 34
                resources = ["Copper"] * 1 + ["Horses"] * 5 + ["Pasture"] * 5
            elif t.terrain == "Plains":
                chance = 34
                resources = ["Horses"] * 1 + ["Copper"] * 3 + ["Wheat"] * 3 + ["Pasture"] * 3 + ["Marble"] * 3
            elif t.terrain == "Grassland":
                chance = 34
                resources = ["Horses"] * 2 + ["Corn"] * 5 + ["Wheat"] * 5 + ["Pasture"] * 3 + ["Spices"]
            elif t.terrain == "Prairie":
                chance = 34
                resources = ["Horses"] * 3 + ["Corn"] * 3 + ["Wheat"] * 5 + ["Pasture"] * 2
            if t.huge_hill == True:
                chance = 15
                resources = ["Iron"] * 5 + ["Stone"] * 10 + ["Gems"] * 2
            if t.hill == True:
                chance = 15
                resources = ["Iron"] * 2 + ["Stone"] * 5 + ["Copper"] * 5 + ["Marble"] * 2 + ["Gems"] * 1
            if t.forest == True:
                chance = 5
                resources = ["Pasture"] * 4 + ["Spices"] * 1
            r = random.randint(0, 99)
            if r < chance:
                t.resource.append(random.choice(resources))
            roll -= 1

    def generate_population(self, tile):
        tile.population = random.randint(500, 1500)

    def generate_hills(self, tile):
        try:
            if tile.height_value > 185 and tile.terrain != "Ocean" and tile.terrain != "Coast":
                tile.huge_hill = True
            elif tile.height_value > 165 and tile.terrain != "Ocean" and tile.terrain != "Coast":
                tile.hill = True
        except:
            print("this tile for some reason has no height_value!")

    def generate_forest(self, tile):
        if tile.terrain in ["Prairie", "Grassland", "Plains"]:
            has_similar_neighbours = False
            for n in tile.get_neighbours():
                if n.forest == False:
                    break
                else:
                    has_similar_neighbours = True
            if has_similar_neighbours:
                tile.forest = True
            r = random.randint(1, 3)
            if r == 3:
                tile.forest = True

    def generate_value(self, tile):
        if tile.terrain == "Prairie":
            tile.value_food = 2
            tile.value_production = 1.5
            tile.value_wealth = 0.5
        elif tile.terrain == "Grassland":
            tile.value_food = 2
            tile.value_production = 1
            tile.value_wealth = 1
        elif tile.terrain == "Plains":
            tile.value_food = 2
            tile.value_production = 2
            tile.value_wealth = 0
        elif tile.terrain == "Swamp":
            tile.value_food = 1
            tile.value_production = 1.5
            tile.value_wealth = 1
        elif tile.terrain == "Desert":
            tile.value_food = 0
            tile.value_production = 2
            tile.value_wealth = 1
        elif tile.terrain == "Steppe":
            tile.value_food = 1
            tile.value_production = 2
            tile.value_wealth = 1.5
        elif tile.terrain == "Ocean":
            tile.value_food = 0.5
            tile.value_production = 0.5
            tile.value_wealth = 0.5
        if tile.hill == True:
            tile.value_production += 1
        elif tile.huge_hill == True:
            tile.value_production += 1.5
        if tile.forest == True: ###
            tile.value_food += 0.5
            tile.value_wealth += 0.25
            tile.value_production += 0.25

width = 40
height = 40
map = Map(width, height)
map.fill_tiles()

for tile in map.tiles:
    print("{}: ({}, {}) --> {}, {}".format(tile.id, tile.x, tile.y, tile.terrain, tile.resource))

root = Tk()
root.geometry = ("600x1000")

size = 13
c = Canvas(root, height = 600, width = 1000, bg = "white")

for tile in map.tiles:
    if tile.terrain == "Grassland":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size,(tile.y + 1) * size, fill = "green")
    elif tile.terrain == "Desert":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "yellow")
    elif tile.terrain == "Swamp":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "olive drab")
    elif tile.terrain == "Steppe":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "orange")
    elif tile.terrain == "Prairie":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "yellow green")
    elif tile.terrain == "Plains":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "light green")
    elif tile.terrain == "Ocean":
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "blue")
    #elif tile.terrain == "Coast":
    #    c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "blue")
    else:
        c.create_rectangle(tile.x * size, tile.y * size, (tile.x + 1) * size, (tile.y + 1) * size, fill = "black")
    if tile.hill == True: # copiei estas 2 linhas de código
        c.create_line(tile.x * size + 1, tile.y * size + size * (2 / 3), tile.x * size + (size / 2), tile.y * size + size / 3,
                               fill="SteelBlue1") #   , tag=("hill1", f.fieldID)
        c.create_line(tile.x * size + size / 2, tile.y * size + size / 3, tile.x * size + size - 1,
                                   tile.y * size + size * (2 / 3), fill="SteelBlue1") #   , tag=("hill2", f.fieldID)
    if tile.huge_hill == True:
        c.create_line(tile.x * size + 1, tile.y * size + size * (2 / 3), tile.x * size + (size / 2), tile.y * size + size / 3,
                               fill="black") #   , tag=("hill1", f.fieldID)
        c.create_line(tile.x * size + size / 2, tile.y * size + size / 3, tile.x * size + size - 1,
                                   tile.y * size + size * (2 / 3), fill="black") #   , tag=("hill2", f.fieldID)
    if "City" in tile.buildings:
        c.create_rectangle((tile.x * size) + (size / 4), (tile.y * size) + (size / 4), ((tile.x + 1) * size) - (size / 4),
                                        (tile.y + 1) * size - size / 4, fill="black")



c.pack()
root.mainloop()
