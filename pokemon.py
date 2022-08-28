import pandas
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
import random
import math

class Pokemon:
    """A class to represent a pokemon

    Args:
        name(str): name of the pokemon
        type(list[str]): type(s) of the pokemon (can have one or two)
        moves(list[str]): moves the pokemon is able to perform
        stats(dict): base stats of the pokemon (health, attack, defense, special attack, special defense, speed)

    Attributes:
        name(str): name of the pokemon
        type(list[str]): type(s) of the pokemon (can have one or two)
        moves(list[str]): moves the pokemon is able to perform
        stats(dict): base stats of the pokemon (health, attack, defense, special attack, special defense, speed)
        health

        
    """

    def __init__(self, name, type, moves, stats):
        self.name = name
        self.type = type
        self.moves = moves
        self.stats = stats
        # self.health = self.stats[0]
        # self.attack = self.stats[1]
        # self.defense = self.stats[2]
        # self.spcatt = self.stats[3]
        # self.spcdef = self.stats[4]
        # self.speed = self.stats[5]
    
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        strtype = "\n".join(self.type)
        convmoves = [str(move) for move in self.moves]
        strmoves = "\n".join(convmoves)
        table = Table(title=f"[b]Pokemon infos[/b] #{self.name}")
        #table = Table("Name", "Type", "Health", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "Moves", title=f"[b]Pokemon infos[/b] #{self.name}")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Health", style="magenta")
        table.add_column("Attack", style="magenta")
        table.add_column("Defense", style="magenta")
        table.add_column("Sp. Attack", style="magenta")
        table.add_column("Sp. Defense", style="magenta")
        table.add_column("Speed", style="magenta")
        table.add_column("Moves", style="dark_orange")
        table.add_row(self.name, strtype, f"{self.stats.get('Health')}", f"{self.stats.get('Attack')}", f"{self.stats.get('Defense')}", f"{self.stats.get('Special Attack')}", f"{self.stats.get('Special Defense')}", f"{self.stats.get('Speed')}", strmoves)
        yield table

    def __repr__(self):
    #     strtype = ", ".join(self.type)
    #     convmoves = [str(move) for move in self.moves]
    #     strmoves = ", ".join(convmoves)
        #return f"Name: {self.name}\nType: {strtype}\nHealth: {self.stats.get('Health')}\nAttack: {self.stats.get('Attack')}\nDefense: {self.stats.get('Defense')}\nSpecial Attack: {self.stats.get('Special Attack')}\nSpecial Defense: {self.stats.get('Special Defense')}\nSpeed: {self.stats.get('Speed')}\nMoves: {strmoves}"
        
        ################## DATAFRAME PANDAS #########################
        # data = [[self.name, strtype, self.stats.get('Health'), self.stats.get('Attack'), self.stats.get('Defense'), self.stats.get('Special Attack'), self.stats.get('Special Defense'), self.stats.get('Speed'), strmoves]]
        # headers=["Name", "Type", "Health", "Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Moves"]
        # return pandas.DataFrame(data, headers).to_string()

        ################# SERIES PANDAS #############################
        # data = [self.name, strtype, self.stats.get('Health'), self.stats.get('Attack'), self.stats.get('Defense'), self.stats.get('Special Attack'), self.stats.get('Special Defense'), self.stats.get('Speed'), strmoves]
        # index=["Name", "Type", "Health", "Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Moves"]
        # return pandas.Series(data=data, index=index).to_string()

        ################ TABLE RICH #################################
        # strtype = "\n".join(zubat.type)
        # convmoves = [str(move) for move in zubat.moves]
        # strmoves = "\n".join(convmoves)
        # table = Table("Name", "Type", "Health", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "Moves")
        # table.add_row(zubat.name, strtype, f"{zubat.stats.get('Health')}", f"{zubat.stats.get('Attack')}", f"{zubat.stats.get('Defense')}", f"{zubat.stats.get('Special Attack')}", f"{zubat.stats.get('Special Defense')}", f"{zubat.stats.get('Speed')}", strmoves)
        # return table
        return self.name

    def damage(self, target, move):
        """
        Example:
            zubat.damage(slowpoke, leechlife)

        Args:
            target(object): Pokemon targetted by the attack
            move(object): move used to attack

        Returns:
            int: points of damage done to the target
        """

        data = [
        [1,1,1,1,1,1/2,1,0,1,1,1,1,1,1,1],
        [2,1,1/2,1/2,1,2,1/2,0,1,1,1,1,1/2,2,1],
        [1,2,1,1,1,1/2,2,1,1,1,2,1/2,1,1,1],
        [1,1,1,1/2,1/2,1/2,2,1/2,1,1,2,1,1,1,1],
        [1,1,0,2,1,2,1/2,1,2,1,1/2,2,1,1,1],
        [0,1/2,2,1,1/2,1,2,1,2,1,1,1,1,2,1],
        [1,1/2,1/2,2,1,1,1,1/2,1/2,1,2,1,2,1,1],
        [0,1,1,1,1,1,1,2,1,1,1,1,0,1,1],
        [1,1,1,1,1,1/2,2,1,1/2,1/2,2,1,1,2,1/2],
        [1,1,1,1,2,2,1,1,2,1/2,1/2,1,1,1,1/2],
        [1,1,1/2,1/2,2,2,1/2,1,1/2,2,1/2,1,1,1,1/2],
        [1,1,2,1,0,1,1,1,1,2,1/2,1/2,1,1,1/2],
        [1,2,1,2,1,1,1,1,1,1,1,1,1/2,1,1],
        [1,1,2,1,2,1,1,1,1,1/2,2,1,1,1/2,2],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
        ]

        headers = ["Normal","Fight","Flying","Poison","Ground","Rock","Bug","Ghost","Fire","Water","Grass","Electric","Psychic","Ice","Dragon"]
        effectiveness = pandas.DataFrame(data, headers, headers)

        level = 1

        critical = 1
        if random.choice(range(0, 255, 1)) < self.stats.get('Speed') / 2:
            critical = (2 * level * self.stats.get('Attack') + 5) / (level + 5)
            print("Critical!")

        attack = 1
        if move.category == 'Physical':
            self.stats.get('Attack')
        if move.category == 'Special':
            attack = self.stats.get('Special Attack')

        defense = 1
        if move.category == 'Physical':
            target.stats.get('Defense')
        if move.category == 'Special':
            defense = target.stats.get('Special ADefense')

        power = move.power

        stab = 1
        if move.type in self.type:
            stab = 1.5

        #For targets that have multiple types, the type effectiveness of a move is the product of its effectiveness against each of the types
        type1 = effectiveness.loc[self.type[0], target.type[0]].squeeze() * effectiveness.loc[self.type[0], target.type[1]].squeeze()

        type2 = effectiveness.loc[self.type[1], target.type[0]].squeeze() * effectiveness.loc[self.type[0], target.type[1]].squeeze()
        
        randomnb = random.choice(range(217, 255, 1)) / 255

        return ((((((2 * level * critical) / 5) + 2) * power * attack / defense) / 50) + 2) * stab * type1 * type2 * randomnb

class Move:
    """A class to represent a move to be performed by a Pokemon"""
    def __init__(self, name, type, category, power):
        """Initializes Move objects attributes
        
        Args:
            name(str): name of the move
            type(str): type of the move
            category(str): move can be 'physical', 'special', or 'status'
            power(int): attack power    
        
        Returns:
            None
        """
        self.name = name
        self.type = type
        self.category = category
        self.power = power

    def __repr__(self):
        """Defines string representation of Move objects"""
        return self.name

    # def __repr__(self):
    #     return pandas.Series(self.__dict__).to_string()

#**************************
#**********MOVES***********
#**************************

leechlife = Move(name="Leech Life", type="Bug", category="Physical", power=20)

wingattack = Move(name="Wing Attack", type="Flying", category="Physical", power=35)

bite = Move(name="Bite", type="Normal", category="Physical", power=60)

megadrain = Move(name="Mega Drain", type="Grass", category="Special", power=40)

watergun = Move(name="Water Gun", type="Water", category="Special", power=40)

headbutt = Move(name="Headbutt", type="Normal", category="Physical", power=70)

confusion = Move(name="Confusion", type="Psychic", category="Special", power=50)

psychic = Move(name="Psychic", type="Psychic", category="Special", power=90)

#**************************
#*********POKEMONS*********
#**************************

zubat = Pokemon(name="Zubat", type=["Poison", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 35, "Special Attack": 30, "Special Defense": 40, "Speed": 55}, moves=[leechlife, wingattack, bite, megadrain])

slowpoke = Pokemon(name="Slowpoke", type=["Water", "Psychic"], stats={"Health": 90, "Attack": 65, "Defense": 65, "Special Attack": 40, "Special Defense": 40, "Speed": 15}, moves=[headbutt, confusion, watergun, psychic])

#print(pandas.DataFrame.from_dict(zubat.__dict__, orient='index').transpose().to_string())

###########################################
########TYPE EFFECTIVENESS TABLE###########
###########################################

# data = [
# [1,1,1,1,1,1/2,1,0,1,1,1,1,1,1,1],
# [2,1,1/2,1/2,1,2,1/2,0,1,1,1,1,1/2,2,1],
# [1,2,1,1,1,1/2,2,1,1,1,2,1/2,1,1,1],
# [1,1,1,1/2,1/2,1/2,2,1/2,1,1,2,1,1,1,1],
# [1,1,0,2,1,2,1/2,1,2,1,1/2,2,1,1,1],
# [0,1/2,2,1,1/2,1,2,1,2,1,1,1,1,2,1],
# [1,1/2,1/2,2,1,1,1,1/2,1/2,1,2,1,2,1,1],
# [0,1,1,1,1,1,1,2,1,1,1,1,0,1,1],
# [1,1,1,1,1,1/2,2,1,1/2,1/2,2,1,1,2,1/2],
# [1,1,1,1,2,2,1,1,2,1/2,1/2,1,1,1,1/2],
# [1,1,1/2,1/2,2,2,1/2,1,1/2,2,1/2,1,1,1,1/2],
# [1,1,2,1,0,1,1,1,1,2,1/2,1/2,1,1,1/2],
# [1,2,1,2,1,1,1,1,1,1,1,1,1/2,1,1],
# [1,1,2,1,2,1,1,1,1,1/2,2,1,1,1/2,2],
# [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
# ]

# headers = ["Normal","Fight","Flying","Poison","Ground","Rock","Bug","Ghost","Fire","Water","Grass","Electric","Psychic","Ice","Dragon"]
# effectiveness = pandas.DataFrame(data, headers, headers)
#print(effectiveness)
#print(effectiveness.to_string())

###########################################
####################JEU####################
###########################################
dicodeck = {}
deck = [zubat, "poupou", "loulou"]
for pokemon in range(len(deck)):
    dicodeck[pokemon] = deck[pokemon]
print(dicodeck)

decknum = [f"{number} {pokemon}" for number,pokemon in enumerate(deck)]
strdeck = "\n".join(decknum)
print(strdeck)

dicodeck = {pokemon: index for (pokemon, index) in enumerate(deck)}
print(dicodeck)

dicotest = {chiffre: (deck.index(chiffre)+1) for chiffre in deck}
print(dicotest)

# convdeck = [str(pokemon) for pokemon in deck]
# print(convdeck)
# strdeck = "\n".join(convdeck)
# print(strdeck)

#Console().print(zubat)
#Console().print(slowpoke)
# print(zubat.damage(slowpoke,leechlife))
# print(zubat.damage(slowpoke,leechlife))
# print(zubat.damage(slowpoke,leechlife))

# wild = [slowpoke]
# attacker = random.choice(wild)
# print("*****DUEL****")
# print(f"Vous êtes attaqué par {attacker}")
# print(f"Vos pokemons disponibles:\n {strdeck}")
# defendant = input(f"\nQuel pokemon choisis-tu pour te battre contre {attacker}?\n")
# while defendant not in convdeck:
#     defendant = input("Choisis un pokemon de ton deck stp\n")
# print(f"Tu as choisi {defendant} pour te battre contre {attacker}")
# print("Place au combat")
# print("Tes attaques: ")
