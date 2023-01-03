from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
import random
import math

from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, MofNCompleteColumn
from rich.table import Table

import time
from rich.live import Live
from rich.table import Table

from inquirer.themes import Default
import inquirer

import collections
import json

from blessed import Terminal

import inquirer.errors as errors

term = Terminal()

console = Console()

class Theme_perso(Default):
    def __init__(self):
        super().__init__()
        self.Question.brackets_color = term.red
        self.List.selection_color = term.red
        self.List.selection_cursor = "+"

class Move:
    """A class to represent a move to be performed by a Pokemon"""
    def __init__(self, name, type, category, power, accuracy=100, pp=30, effect=None):
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
        self.accuracy = accuracy
        self.pp = pp
        self.effect = effect

    def __repr__(self):
        """Defines string representation of Move objects"""
        return self.name.upper()

    # def __repr__(self):
    #     return pandas.Series(self.__dict__).to_string()


    def effectiveness(self, target):

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

        headers = ['Normal','Fight','Flying','Poison','Ground','Rock','Bug','Ghost','Fire','Water','Grass','Electric','Psychic','Ice','Dragon']
        
        effect = {}

        for i in range(len(data)):
            bytype = {}
            line = data[i]
            for value in range(len(headers)):
                key = headers[value]
                value = line[value]
                bytype[key] = value
            key = headers[i]
            effect[key] = bytype

        #####################################################################################################################################
        #for targets that have multiple types the type effectiveness of a move is the product of its effectiveness against each of the types#
        #####################################################################################################################################

        if type(target.type) == list:
            return effect[self.type][target.type[0]] * effect[self.type][target.type[1]]

        else:
            return effect[self.type][target.type]

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
        convmoves = [str(move.name) for move in self.moves]
        strmoves = "\n".join(convmoves)
        table = Table(title=f"[b]POKéMON summary[/b] #{self.name}")
        #table = Table("Name", "Type", "Health", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "Moves", title=f"[b]Pokemon infos[/b] #{self.name}")
        table.add_column("Name", style="cyan")
        table.add_column("Type(s)", style="green")
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
        #strtype = ", ".join(self.type)
        #convmoves = [str(move) for move in self.moves]
        #strmoves = ", ".join(convmoves)
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
        return self.name.upper()


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

        # headers = ['Normal','Fight','Flying','Poison','Ground','Rock','Bug','Ghost','Fire','Water','Grass','Electric','Psychic','Ice','Dragon']
        
        # effect = {}

        # for i in range(len(data)):
        #     bytype = {}
        #     line = data[i]
        #     for value in range(len(headers)):
        #         key = headers[value]
        #         value = line[value]
        #         bytype[key] = value
        #     key = headers[i]
        #     effect[key] = bytype    

        level = 1

        critical = 1
        if random.choice(range(0, 255, 1)) < self.stats.get('Speed') / 2:
            print('A critical hit!')
            critical = (2 * level * self.stats.get('Attack') + 5) / (level + 5)

        attack = 1
        if move.category == 'Physical':
            self.stats.get('Attack')
        if move.category == 'Special':
            attack = self.stats.get('Special Attack')

        defense = 1
        if move.category == 'Physical':
            target.stats.get('Defense')
        if move.category == 'Special':
            defense = target.stats.get('Special Defense')

        power = move.power

        STAB = 1
        if move.type in self.type:
            STAB = 1.5

        nbrandom = random.choice(range(217, 255, 1)) / 255

        #####################################################################################################################################
        #for targets that have multiple types the type effectiveness of a move is the product of its effectiveness against each of the types#
        #####################################################################################################################################
        
        #type1 = effectiveness.loc[self.type[0], target.type[0]].squeeze() * effect.loc[self.type[0], target.type[1]].squeeze()

        #type2 = effectiveness.loc[self.type[1], target.type[0]].squeeze() * effect.loc[self.type[0], target.type[1]].squeeze()

        #type1 = effect[self.type[0]][target.type[0]] * effect[self.type[0]][target.type[1]]
        #type2 = effect[self.type[1]][target.type[0]] * effect[self.type[0]][target.type[1]]
        #return ((((((2 * level * critical) / 5) + 2) * power * attack / defense) / 50) + 2) * STAB * type1 * type2 * nbrandom
        
        # type1 = effect[move.type][target.type[0]]
        # print(type1)

        # type2 = effect[move.type][target.type[1]]
        # print(type2)

        print(f"(--effectiveness: {move.effectiveness(target)})")
        if move.effectiveness(target) >= 2:
            print("It's super effective!")
        if move.effectiveness(target) == 0.5:
            print("It's not very effective...")
        if move.effectiveness(target) == 0:
            print(f"It doesn't affect {target}...")

        #return ((((((2 * level * critical) / 5) + 2) * power * attack / defense) / 50) + 2) * STAB * move.effectiveness(target) * nbrandom
        return round(((((((2 * level * critical) / 5) + 2) * power * attack / defense) / 50) + 2) * STAB * move.effectiveness(target) * nbrandom)


#**************************
#**********MOVES***********
#**************************

leechseed = Move(name="Leech Seed", type="Grass", category="Special", power=0, accuracy=90, pp=10, effect="Drain")

constrict = Move(name="Constrict", type="Normal", category="Physical", power=10, accuracy=100, pp=35)

wrap = Move(name="Wrap", type="Normal", category="Physical", power=15, accuracy=85, pp=20)

furyattack = Move(name="Fury Attack", type="Normal", category="Physical", power=15, accuracy=90, pp=20)

poisonsting = Move(name="Poison Sting", type="Poison", category="Physical", power=15, accuracy=100, pp=35)

leechlife = Move(name="Leech Life", type="Bug", category="Physical", power=20, accuracy=100, pp=15, effect="Drain")

rage = Move(name="Rage", type="Normal", category="Physical", power=20, accuracy=100, pp=20)

vinewhip = Move(name="Vine Whip", type="Grass", category="Special", power=35, accuracy=100, pp=10)

tackle = Move(name="Tackle", type="Normal", category="Physical", power=35, accuracy=95, pp=35)

wingattack = Move(name="Wing Attack", type="Flying", category="Physical", power=35, accuracy=100, pp=35)

peck = Move(name="Peck", type="Flying", category="Physical", power=35, accuracy=100, pp=35)

megadrain = Move(name="Mega Drain", type="Grass", category="Special", power=40)

gust = Move(name="Gust", type="Flying", category="Special", power=40, accuracy=100, pp=35)

watergun = Move(name="Water Gun", type="Water", category="Special", power=40, accuracy=100, pp=25)

acid = Move(name="Acid", type="Poison", category="Physical", power=40, accuracy=100, pp=30)

ember = Move(name="Ember", type="Fire", category="Special", power=40, accuracy=100, pp=25)

scratch = Move(name="Scratch", type="Normal", category="Physical", power=40)

quickattack = Move(name="Quick Attack", type="Normal", category="Physical", power=40, accuracy=100, pp=30)

thundershock = Move(name="Thunder Shock", type="Electric", category="Special", power=45)

confusion = Move(name="Confusion", type="Psychic", category="Special", power=50, accuracy=100, pp=25)

razorleaf = Move(name="Razor Leaf", type="Grass", category="Special", power=55, accuracy=95, pp=25)

bite = Move(name="Bite", type="Normal", category="Physical", power=60, accuracy=100, pp=25)

thunderwave = Move(name="Thunder Wave", type="Electric", category="Physical", power=65)

stomp = Move(name="Stomp", type="Normal", category="Physical", power=65, accuracy=100, pp=20)

hornattack = Move(name="Horn Attack", type="Normal", category="Physical", power=65, accuracy=100, pp=25)

slash = Move(name="Slash", type="Normal", category="Physical", power=70, accuracy=100, pp=20)

headbutt = Move(name="Headbutt", type="Normal", category="Physical", power=70, accuracy=100, pp=15)

rockslide = Move(name="Rock Slide", type="Rock", category="Physical", power=75, accuracy=90, pp=10)

bodyslam = Move(name="Body Slam", type="Normal", category="Physical", power=85, accuracy=100, pp=15)

psychic = Move(name="Psychic", type="Psychic", category="Special", power=90, accuracy=100, pp=10)

#####################################TROP FORT####################################################
flamethrower = Move(name="Flamethrower", type="Fire", category="Special", power=95)

doubleedge = Move(name="Double Edge", type="Normal", category="Physical", power=100, accuracy=100, pp=15)

earthquake = Move(name="Earthquake", type="Ground", category="Physical", power=100)

solarbeam = Move(name="Solar Beam", type="Grass", category="Special", power=120)

#**************************
#*********POKEMONS*********
#**************************

zubat = Pokemon(name="Zubat", type=["Poison", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 35, "Special Attack": 30, "Special Defense": 40, "Speed": 55}, moves=[leechlife, wingattack, bite, megadrain])

slowpoke = Pokemon(name="Slowpoke", type=["Water", "Psychic"], stats={"Health": 90, "Attack": 65, "Defense": 65, "Special Attack": 40, "Special Defense": 40, "Speed": 15}, moves=[rage, confusion, watergun, psychic])

bulbasaur = Pokemon(name="Bulbasaur", type=["Grass", "Poison"], stats={"Health": 45, "Attack": 49, "Defense": 49, "Special Attack": 65, "Special Defense": 65, "Speed": 45}, moves=[tackle, vinewhip, razorleaf, leechseed])

pidgey = Pokemon(name="Pidgey", type=["Normal", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 40, "Special Attack": 35, "Special Defense": 35, "Speed": 56}, moves=[gust, quickattack, wingattack, rage])

venonat = Pokemon(name="Venonat", type=["Bug", "Poison"], stats={"Health": 60, "Attack": 55, "Defense": 50, "Special Attack": 40, "Special Defense": 40, "Speed": 45}, moves=[psychic, leechlife, confusion, tackle])

rhyhorn = Pokemon(name="Rhyhorn", type=["Ground", "Rock"], stats={"Health": 80, "Attack": 85, "Defense": 95, "Special Attack": 30, "Special Defense": 30, "Speed": 25}, moves=[furyattack, rockslide, hornattack, stomp])

farfetchd = Pokemon(name="Farfetch'd", type=["Normal", "Flying"], stats={"Health": 52, "Attack": 65, "Defense": 55, "Special Attack": 58, "Special Defense": 58, "Speed": 60}, moves=[bodyslam, slash, furyattack, peck])

tentacool = Pokemon(name="Tentacool", type=["Water", "Poison"], stats={"Health": 40, "Attack": 40, "Defense": 35, "Special Attack": 100, "Special Defense": 100, "Speed": 70}, moves=[acid, wrap, constrict, watergun])

charmander = Pokemon(name="Charmander", type=["Fire"], stats={"Health": 39, "Attack": 52, "Defense": 43, "Special Attack": 50, "Special Defense": 50, "Speed": 65}, moves=[scratch, ember, slash, rage])

squirtle = Pokemon(name="Squirtle", type=["Water"], stats={"Health": 44, "Attack": 48, "Defense": 65, "Special Attack": 50, "Special Defense": 50, "Speed": 43}, moves=[tackle, watergun, bite, rage])
mankey = Pokemon(name="Squirtle", type=["Water"], stats={"Health": 44, "Attack": 48, "Defense": 65, "Special Attack": 50, "Special Defense": 50, "Speed": 43}, moves=[tackle, watergun, bite, rage])
weedle = Pokemon(name="Squirtle", type=["Bug", "Poison"], stats={"Health": 40, "Attack": 35, "Defense": 30, "Special Attack": 20, "Special Defense": 20, "Speed": 50}, moves=[tackle, watergun, bite, rage])
pikachu = Pokemon(name="Pikachu", type=["Water"], stats={"Health": 35, "Attack": 55, "Defense": 30, "Special Attack": 50, "Special Defense": 50, "Speed": 90}, moves=[tackle, watergun, bite, rage])
gastly = Pokemon(name="Gastly", type=["Ghost", "Poison"], stats={"Health": 30, "Attack": 35, "Defense": 30, "Special Attack": 100, "Special Defense": 100, "Speed": 80}, moves=[tackle, watergun, bite, rage])
magnemite = Pokemon(name="Magnemite", type=["Electric"], stats={"Health": 25, "Attack": 35, "Defense": 70, "Special Attack": 95, "Special Defense": 95, "Speed": 45}, moves=[tackle, watergun, bite, rage])


###########################################
############POKEMONS-EN-JEU################
###########################################

wild_pokemons = [rhyhorn, slowpoke]

my_pokemons = [bulbasaur, zubat, tentacool, pidgey]

###########################################
############VALEURS DE DEPART##############
###########################################

foe = random.choice(wild_pokemons)

hp_foe = foe.stats.get('Health')

usable_pokemons = my_pokemons

my_pokemons_hp = {}
for pokemon in usable_pokemons:
    key = pokemon
    value = pokemon.stats.get('Health')
    my_pokemons_hp[key] = value
print(my_pokemons_hp)

fighter = usable_pokemons[0]
hp_fighter = my_pokemons_hp[fighter]

def prompt_fight():
    choice_move = [
    inquirer.List('move',
                    message=f"What should {fighter} do?",
                    choices=fighter.moves,
                ),
    ]
    
    choice_move = inquirer.prompt(choice_move)
    choice_move = choice_move['move']
    return choice_move

def prompt_change():
    choice_pokemon = [
    inquirer.List('pokemon',
                    message=f"Choose a Pokémon",
                    choices=my_pokemons,
                ),
    ]

    choice_pokemon = inquirer.prompt(choice_pokemon)
    fighter = choice_pokemon['pokemon']
    return fighter

def prompt_action():
    choice_action = [
    inquirer.List('action',
                    message=f"What should {fighter} do?",
                    #choices=['Fight', 'Pokémons', 'Run'],
                    choices=['FIGHT', 'POKéMON', 'RUN', f"{fighter} SUMMARY"],
                ),
    ]

    choice_action = inquirer.prompt(choice_action)
    choice_action = choice_action['action']
    return choice_action

def perform_move(move):
    print(f"{fighter} used {move}!")
    return hp_foe - fighter.damage(foe,move)

###########################################
###################COMBAT##################
###########################################

print(f"\nWild {foe} appeared!\n")

while usable_pokemons != 0:
#while usable_pokemons != 0 or hp_foe > 0:
    print("(boucle 1)")
    #hp_fighter = fighter.stats.get('Health')
    #hp_fighter = my_pokemons_hp[fighter]
    if hp_foe <= 0:
        print("(fin du combat #boucle2)")
        break
    # elif hp_fighter == fighter.stats.get('Health'):
    #     #trouver meilleur moyen de trouver que c'est la première action, quid si dommage infligé = 0
    #     print("(première action)")
    #     #print(f"Go! {usable_pokemons[0]}!\n")
    #     #print(f"Go! {fighter}!\n")
    # else:
    #     print("(changement de pokemon)")
    #     choice_pokemon = [
    #     inquirer.List('pokemon',
    #                     message=f"Choose a Pokémon",
    #                     choices=my_pokemons,
    #                 ),
    #     ]
    #     choice_pokemon = inquirer.prompt(choice_pokemon)
    #     fighter = choice_pokemon['pokemon']
    #     #réinitialisation de la valeur ATTENTION pas si pokémon déjà utilisé
    #     hp_fighter = my_pokemons_hp[fighter]
    #     #print(f"Go! {fighter}!\n")
    elif len(usable_pokemons) != 4:
        print("(changement de pokemon)")
        choice_pokemon = [
        inquirer.List('pokemon',
                        message=f"Choose a Pokémon",
                        choices=my_pokemons,
                    ),
        ]
        choice_pokemon = inquirer.prompt(choice_pokemon)
        fighter = choice_pokemon['pokemon']
        hp_fighter = my_pokemons_hp[fighter]
        
    print(f"Go! {fighter}!\n")
    print(f"(hp fighter {fighter} {hp_fighter})")

    while hp_fighter > 0:
        print("(boucle 2)")
        # choice_action = [
        #     inquirer.List('action',
        #                     message=f"What should {fighter} do?",
        #                     choices=['Fight', 'Pokémons', 'Run'],
        #                     #choices=['Fight', 'Pokémons', 'Run', f"{fighter.name} summary"],
        #                 ),
        #     ]

        # choice_action = inquirer.prompt(choice_action)
        # choice_action = choice_action['action']

        # if choice_action == 'Fight':
        #     choice_move = [
        #     inquirer.List('move',
        #                     message=f"What should {fighter} do?",
        #                     choices=fighter.moves,
        #                 ),
        #     ]
            
        #     choice_move = inquirer.prompt(choice_move)
        #     print(f"{fighter} used {choice_move['move']}!")
        #     print(fighter.damage(foe,choice_move['move']))

        #     print(f"(--- hp du foe {foe} avant: {hp_foe})")
        #     hp_foe = hp_foe - fighter.damage(foe,choice_move['move'])
        #     print(f"(--- hp du foe {foe} après: {hp_foe})")

        #     if hp_foe <= 0:
        #         print(f"Wild {foe} fainted!\n")
        #         print("(fin du combat)")
        #         break

        #     if hp_fighter <= 0:
        #         print(usable_pokemons)
        #         print(f"{fighter} fainted!\n")
        #         usable_pokemons.remove(fighter)
        #         print(usable_pokemons)
        #         choice = input("Use next POKéMON? (y/n)")
        #         while choice.lower() != 'y' and choice.lower() != 'n':
        #             choice = input("Use next POKéMON? (y/n)")
        #         if choice == 'y':
        #             break

        # if choice_action == 'Pokémons':
        #     choice_pokemon = [
        #     inquirer.List('pokemon',
        #                     message=f"Choose a Pokémon",
        #                     choices=my_pokemons,
        #                 ),
        #     ]

        #     choice_pokemon = inquirer.prompt(choice_pokemon)
        #     fighter = choice_pokemon['pokemon']
        #     hp_fighter = my_pokemons_hp[fighter]

        # if choice_action == 'Run':
        #     print("You can't run")

#############avec fonction prompt_action()###########
        chosen_action = prompt_action()
        if chosen_action == 'FIGHT':
            chosen_move = prompt_fight()

            print(f"{fighter} used {chosen_move}!")
            print(fighter.damage(foe,chosen_move))
            print(f"(--- hp du foe {foe} avant: {hp_foe})")
            hp_foe = hp_foe - fighter.damage(foe,chosen_move)
            print(f"(--- hp du foe {foe} après: {hp_foe})")

            if hp_foe <= 0:
                print(f"Wild {foe} fainted!\n")
                print("(fin du combat)")
                break

            if hp_fighter <= 0:
                print(usable_pokemons)
                print(f"{fighter} fainted!\n")
                usable_pokemons.remove(fighter)
                print(usable_pokemons)
                choice = input("Use next POKéMON? (y/n)")
                while choice.lower() != 'y' and choice.lower() != 'n':
                    choice = input("Use next POKéMON? (y/n)")
                if choice == 'y':
                    break

        if chosen_action == 'POKéMON':
            fighter = prompt_change()
            hp_fighter = my_pokemons_hp[fighter]

        while chosen_action == 'RUN':
            print("You can't run\n")
            chosen_action = prompt_action()

        while chosen_action == f"{fighter} SUMMARY":
            Console().print(fighter)
            chosen_action = prompt_action()

        ################### foe's turn #################
        print("...")
        foe_move = random.choice(foe.moves)
        print(f"Foe {foe} used {foe_move}")
        print(f"--- hp du fighter {fighter} avant: {hp_fighter}")
        hp_fighter = hp_fighter - foe.damage(fighter,foe_move)
        my_pokemons_hp[fighter] = hp_fighter
        print(f"--- hp du fighter {fighter} après: {hp_fighter}")
        print(my_pokemons_hp)
        ################################################

        if hp_foe <= 0:
            print(f"Wild {foe} fainted!\n")
            print("Fin du combat")
            break

        if hp_fighter <= 0:
            print(usable_pokemons)
            print(f"{fighter} fainted!\n")
            usable_pokemons.remove(fighter)
            print(usable_pokemons)
            choice = input("Use next POKéMON? (y/n)")
            while choice.lower() != 'y' and choice.lower() != 'n':
                choice = input("Use next POKéMON? (y/n)")
            if choice == 'y':
                break
            elif choice == 'n':
                print("You can't escape\n")

print("<player> is out of useable Pokémon!")
    
###########################################
################INTERFACE##################
###########################################

layout = Layout(name="root")

layout.split(
    Layout(name="pokemons"),
    Layout(name="messages"),
)
layout["pokemons"].split_column(
    Layout(name="foe"),
    Layout(name="player"),
)
layout["foe"].split_row(
    Layout(name="hp", ratio=2),
    Layout(name="name"),
)

layout["player"].split_row(
    Layout(name="name"),
    Layout(name="hp", ratio=2),
)

layout["pokemons"].size = 10
layout["messages"].size = 8

hp_progress_foe = Progress(
    "{task.description}",
    SpinnerColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
)

hp_progress_player = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    MofNCompleteColumn(separator='/', table_column=None),
)

hp_progress_foe.add_task("[magenta]HP")
hp_progress_player.add_task("[red]HP", total=200)

progress_table_player = Table.grid(expand=True)
progress_table_player.add_row(
    Panel(hp_progress_player, border_style="green", padding=(1, 2))
)

progress_table_foe = Table.grid(expand=True)
progress_table_foe.add_row(
    Panel(hp_progress_foe, border_style="magenta", padding=(1, 2))
)

pokemon_name = Table.grid(padding=1, expand=True)
pokemon_name.add_column(style="b cyan2", justify="left")
pokemon_name.add_column(style="b magenta")
pokemon_name.add_column(style="b plum1", justify="right")
pokemon_name.add_row(
    "Zubat",
    "|",
    "Lvl:1",
)

pokemon_name_panel = Panel(pokemon_name, border_style="red", padding=(1, 2)#, height=5
)

pokemon_panel_foe = Table.grid(padding=1, expand=True)
pokemon_panel_foe.add_column(style="b magenta", ratio=1)
pokemon_panel_foe.add_column(justify="right", style="b cyan", ratio=2)
pokemon_panel_foe.add_row(
    pokemon_name_panel,
    progress_table_foe,
)

pokemon_panel_player = Table.grid(padding=1, expand=True)
pokemon_panel_player.add_column(style="b magenta", ratio=2)
pokemon_panel_player.add_column(justify="right", style="b cyan", ratio=1)
pokemon_panel_player.add_row(
    progress_table_player,
    pokemon_name_panel,
)

def print_message(message):
    instructions = Table.grid(padding=1, expand=True)
    instructions.add_row(message)

    message_panel = Panel(instructions,
    box=box.ROUNDED,
    padding=(1, 2),
    title="[b orange1]message panel",
    border_style="cyan")

    return message_panel

# message = "#######"
# instructions = Table.grid(padding=1, expand=True)
# instructions.add_row(message)

# message_panel = Panel(instructions,
#     box=box.ROUNDED,
#     padding=(1, 2),
#     title="[b orange1]message panel",
#     border_style="cyan")

interface = Panel(
        Align.center(
            Group(pokemon_panel_foe,pokemon_panel_player, print_message("###")),
            vertical="middle",
        ),
        box=box.DOUBLE,
        padding=(1, 2),
        title="[b blue_violet]POKEMON GAME",
        title_align='right',
        border_style="blue_violet",
    )

interface_layout = Panel(
        layout,
        box=box.DOUBLE,
        padding=(1, 1),
        title="[b blue_violet]POKEMON GAME",
        title_align='right',
        border_style="blue_violet",
        width=80,
        height=22,
    )

layout["messages"].update(print_message("WILD POKEMON"))
layout["pokemons"]["foe"]["hp"].update(progress_table_foe)
layout["pokemons"]["foe"]["name"].update(pokemon_name_panel)
layout["pokemons"]["player"]["hp"].update(progress_table_player)
layout["pokemons"]["player"]["name"].update(pokemon_name_panel)

layout["messages"].update(print_message("ZUBAT ATTACK"))

# print(f"{answers['your_pokemon'].upper()} used !")
# print("TRAINER CHRISTINA would like to battle!")
# print("TRAINER CHRISTINA send out ")