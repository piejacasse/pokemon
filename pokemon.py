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

import pprint
import tkinter
from tkinter import *

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

        #print(f"(--effectiveness: {move.effectiveness(target)})")
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

leechseed = Move(name="Leech Seed", type="Grass", category="Special", power=0, accuracy=90, pp=10, effect="drain")
constrict = Move(name="Constrict", type="Normal", category="Physical", power=10, accuracy=100, pp=35)
wrap = Move(name="Wrap", type="Normal", category="Physical", power=15, accuracy=85, pp=20)
furyattack = Move(name="Fury Attack", type="Normal", category="Physical", power=15, accuracy=90, pp=20)
poisonsting = Move(name="Poison Sting", type="Poison", category="Physical", power=15, accuracy=100, pp=35)
leechlife = Move(name="Leech Life", type="Bug", category="Physical", power=20, accuracy=100, pp=15, effect="drain")
rage = Move(name="Rage", type="Normal", category="Physical", power=20, accuracy=100, pp=20)
lick = Move(name="Lick", type="Ghost", category="Physical", power=20, accuracy=100, pp=30)
vinewhip = Move(name="Vine Whip", type="Grass", category="Special", power=35, accuracy=100, pp=10)
tackle = Move(name="Tackle", type="Normal", category="Physical", power=35, accuracy=95, pp=35)
wingattack = Move(name="Wing Attack", type="Flying", category="Physical", power=35, accuracy=100, pp=35)
peck = Move(name="Peck", type="Flying", category="Physical", power=35, accuracy=100, pp=35)
megadrain = Move(name="Mega Drain", type="Grass", category="Special", power=40, accuracy=100, pp=10, effect="drain")
gust = Move(name="Gust", type="Flying", category="Special", power=40, accuracy=100, pp=35)
watergun = Move(name="Water Gun", type="Water", category="Special", power=40, accuracy=100, pp=25)
acid = Move(name="Acid", type="Poison", category="Physical", power=40, accuracy=100, pp=30)
ember = Move(name="Ember", type="Fire", category="Special", power=40, accuracy=100, pp=25)
scratch = Move(name="Scratch", type="Normal", category="Physical", power=40, accuracy=100, pp=35)
quickattack = Move(name="Quick Attack", type="Normal", category="Physical", power=40, accuracy=100, pp=30)
thundershock = Move(name="Thunder Shock", type="Electric", category="Special", power=45, accuracy=100, pp=30)
lowkick = Move(name="Low Kick", type="Fight", category="Physical", power=50, accuracy=90, pp=20)
confusion = Move(name="Confusion", type="Psychic", category="Special", power=50, accuracy=100, pp=25)
rockthrow = Move(name="Rock Throw", type="Rock", category="Physical", power=50, accuracy=65, pp=15)
razorleaf = Move(name="Razor Leaf", type="Grass", category="Special", power=55, accuracy=95, pp=25)
bite = Move(name="Bite", type="Normal", category="Physical", power=60, accuracy=100, pp=25)
swift = Move(name="Swift", type="Normal", category="Physical", power=60, accuracy=100, pp=20)
bubblebeam = Move(name="Bubble Beam", type="Water", category="Special", power=65, accuracy=100, pp=20)
stomp = Move(name="Stomp", type="Normal", category="Physical", power=65, accuracy=100, pp=20)
hornattack = Move(name="Horn Attack", type="Normal", category="Physical", power=65, accuracy=100, pp=25)
slash = Move(name="Slash", type="Normal", category="Physical", power=70, accuracy=100, pp=20)
headbutt = Move(name="Headbutt", type="Normal", category="Physical", power=70, accuracy=100, pp=15)
rockslide = Move(name="Rock Slide", type="Rock", category="Physical", power=75, accuracy=90, pp=10)
strength = Move(name="Strength", type="Normal", category="Physical", power=80, accuracy=100, pp=15)
bodyslam = Move(name="Body Slam", type="Normal", category="Physical", power=85, accuracy=100, pp=15)
psychic = Move(name="Psychic", type="Psychic", category="Special", power=90, accuracy=100, pp=10)
furyswipes = Move(name="Fury Swipes", type="Normal", category="Physical", power=18, accuracy=80, pp=15, effect="multistrike")
thunderbolt = Move(name="Thunder Bolt", type="Electric", category="Special", power=95, accuracy=100, pp=15)
petaldance = Move(name="Petal Dance", type="Grass", category="Physical", power=70, accuracy=100, pp=20)
dreameater = Move(name="Dream Eater", type="Grass", category="Physical", power=70, accuracy=100, pp=20)
flamethrower = Move(name="Flamethrower", type="Fire", category="Special", power=95)
doubleedge = Move(name="Double Edge", type="Normal", category="Physical", power=100, accuracy=100, pp=15)
earthquake = Move(name="Earthquake", type="Ground", category="Physical", power=100, accuracy=100, pp=10)
solarbeam = Move(name="Solar Beam", type="Grass", category="Special", power=120)
twineedle = Move(name="Twineedle", type="Bug", category="Physical", power=25, accuracy=100, pp=20, effect="multistrike")
pinmissile = Move(name="Pin Missile", type="Bug", category="Physical", power=25, accuracy=95, pp=20, effect="multistrike")
fireblast = Move(name="Fire Blast", type="Fire", category="Special", power=110, accuracy=85, pp=5)
pound = Move(name="Pound", type="Normal", category="Physical", power=40, accuracy=100, pp=35)
lick = Move(name="Lick", type="Ghost", category="Physical", power=30, accuracy=100, pp=30)
icepunch = Move(name="Ice Punch", type="Ice", category="Physical", power=75, accuracy=100, pp=15)
thunder = Move(name="Thunder", type="Electric", category="Special", power=110, accuracy=70, pp=10)

#**************************
#*********POKEMONS*********
#**************************

gastly = Pokemon(name="Gastly", type=["Ghost", "Poison"], stats={"Health": 30, "Attack": 35, "Defense": 30, "Special Attack": 100, "Special Defense": 100, "Speed": 80}, moves=[lick, megadrain, thunderbolt, dreameater])
magnemite = Pokemon(name="Magnemite", type="Electric", stats={"Health": 25, "Attack": 35, "Defense": 70, "Special Attack": 95, "Special Defense": 95, "Speed": 45}, moves=[tackle, thundershock, thunderbolt, swift])
butterfree = Pokemon(name="Butterfree", type=["Bug", "Poison"], stats={"Health": 40, "Attack": 35, "Defense": 30, "Special Attack": 20, "Special Defense": 20, "Speed": 50}, moves=[tackle, gust, megadrain, confusion])
tentacool = Pokemon(name="Tentacool", type=["Water", "Poison"], stats={"Health": 40, "Attack": 40, "Defense": 35, "Special Attack": 100, "Special Defense": 100, "Speed": 70}, moves=[acid, wrap, constrict, watergun])
zubat = Pokemon(name="Zubat", type=["Poison", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 35, "Special Attack": 30, "Special Defense": 40, "Speed": 55}, moves=[leechlife, wingattack, bite, megadrain])
pidgey = Pokemon(name="Pidgey", type=["Normal", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 40, "Special Attack": 35, "Special Defense": 35, "Speed": 56}, moves=[gust, quickattack, wingattack, rage])
squirtle = Pokemon(name="Squirtle", type="Water", stats={"Health": 44, "Attack": 48, "Defense": 65, "Special Attack": 50, "Special Defense": 50, "Speed": 43}, moves=[tackle, watergun, bite, bubblebeam])
bulbasaur = Pokemon(name="Bulbasaur", type=["Grass", "Poison"], stats={"Health": 45, "Attack": 49, "Defense": 49, "Special Attack": 65, "Special Defense": 65, "Speed": 45}, moves=[tackle, vinewhip, razorleaf, leechseed])
charmander = Pokemon(name="Charmander", type="Fire", stats={"Health": 39, "Attack": 52, "Defense": 43, "Special Attack": 50, "Special Defense": 50, "Speed": 65}, moves=[scratch, ember, slash, bodyslam])
psyduck = Pokemon(name="Psyduck", type="Water", stats={"Health": 50, "Attack": 52, "Defense": 48, "Special Attack": 50, "Special Defense": 50, "Speed": 55}, moves=[confusion, tackle, furyswipes, watergun])
venonat = Pokemon(name="Venonat", type=["Bug", "Poison"], stats={"Health": 60, "Attack": 55, "Defense": 50, "Special Attack": 40, "Special Defense": 40, "Speed": 45}, moves=[psychic, leechlife, confusion, tackle])
geodude = Pokemon(name="Geodude", type=["Rock", "Ground"], stats={"Health": 40, "Attack": 80, "Defense": 100, "Special Attack": 30, "Special Defense": 30, "Speed": 20}, moves=[tackle, rockthrow, strength, earthquake])

beedrill = Pokemon(name="Beedrill", type=["Bug", "Poison"], stats={"Health": 65, "Attack": 80, "Defense": 40, "Special Attack": 45, "Special Defense": 45, "Speed": 75}, moves=[rage, furyattack, pinmissile, twineedle])
farfetchd = Pokemon(name="Farfetch'd", type=["Normal", "Flying"], stats={"Health": 52, "Attack": 65, "Defense": 55, "Special Attack": 58, "Special Defense": 58, "Speed": 60}, moves=[bodyslam, slash, furyattack, peck])
slowpoke = Pokemon(name="Slowpoke", type=["Water", "Psychic"], stats={"Health": 90, "Attack": 65, "Defense": 65, "Special Attack": 40, "Special Defense": 40, "Speed": 15}, moves=[rage, confusion, watergun, psychic])
mankey = Pokemon(name="Mankey", type="Fight", stats={"Health": 40, "Attack": 80, "Defense": 35, "Special Attack": 35, "Special Defense": 35, "Speed": 70}, moves=[furyswipes, lowkick, scratch, rage])
vileplume = Pokemon(name="Vileplume", type=["Grass", "Poison"], stats={"Health": 75, "Attack": 80, "Defense": 85, "Special Attack": 100, "Special Defense": 100, "Speed": 50}, moves=[acid, petaldance, megadrain])
sandshrew = Pokemon(name="Sandshrew", type="Ground", stats={"Health": 50, "Attack": 75, "Defense": 85, "Special Attack": 30, "Special Defense": 30, "Speed": 40}, moves=[scratch, slash, poisonsting, furyswipes])
rhyhorn = Pokemon(name="Rhyhorn", type=["Ground", "Rock"], stats={"Health": 80, "Attack": 85, "Defense": 95, "Special Attack": 30, "Special Defense": 30, "Speed": 25}, moves=[furyattack, rockslide, hornattack, stomp])
ninetales = Pokemon(name="Ninetales", type="Fire", stats={"Health": 73, "Attack":76 ,"Defense": 75, "Special Attack": 100, "Special Defense": 100, "Speed": 100}, moves=[doubleedge, ember, quickattack, fireblast])
jynx = Pokemon(name="Jynx", type=["Ice", "Psychic"], stats={"Health": 65, "Attack":50 ,"Defense": 35, "Special Attack": 95, "Special Defense": 95, "Speed": 95}, moves=[pound, lick, bodyslam, icepunch])
jolteon = Pokemon(name="Jolteon", type="Electric", stats={"Health": 65, "Attack":65 ,"Defense": 60, "Special Attack": 110, "Special Defense": 110, "Speed": 130}, moves=[quickattack, thunder, thundershock, pinmissile])

###########################################
############POKEMONS-EN-JEU################
###########################################

#wild_pokemons = [rhyhorn, slowpoke]
#my_pokemons = [bulbasaur, zubat, tentacool, pidgey]

trainer_team = [beedrill, farfetchd, slowpoke, mankey, vileplume, sandshrew, rhyhorn, ninetales, jynx, jolteon]

available_pokemons = [gastly, magnemite, butterfree, tentacool, zubat, pidgey, squirtle, bulbasaur, charmander, psyduck, venonat, geodude]

###########################################
############VALEURS DE DEPART##############
###########################################

#foe = random.choice(wild_pokemons)
#hp_foe = foe.stats.get('Health')

player_team = set()

#trainer_pokemon = ""

def team_hp(team):
    team_hp = {}
    for pokemon in team:
        key = pokemon
        value = pokemon.stats.get('Health')
        team_hp[key] = value
    return team_hp

def prompt_team():
    prompt_team = [
    inquirer.List('team',
                    message=f"Choose a Pokémon",
                    choices=available_pokemons,
                ),
    ]
    prompt_team = inquirer.prompt(prompt_team)
    pokemon = prompt_team['team']
    player_team.add(pokemon)

def prompt_fight():
    choice_move = [
    inquirer.List('move',
                    message=f"What should {player_pokemon} do?",
                    choices=player_pokemon.moves,
                ),
    ]
    
    choice_move = inquirer.prompt(choice_move)
    choice_move = choice_move['move']
    return choice_move

def prompt_change():
    choice_pokemon = [
    inquirer.List('pokemon',
                    message=f"Choose a Pokémon",
                    choices=player_team,
                ),
    ]

    choice_pokemon = inquirer.prompt(choice_pokemon)
    player_pokemon = choice_pokemon['pokemon']
    return player_pokemon

def prompt_action():
    choice_action = [
    inquirer.List('action',
                    message=f"What should {player_pokemon} do?",
                    #choices=['Fight', 'Pokémons', 'Run'],
                    choices=['FIGHT', 'CHANGE POKéMON', 'RUN', f"{player_pokemon} SUMMARY"],
                ),
    ]

    choice_action = inquirer.prompt(choice_action)
    choice_action = choice_action['action']
    return choice_action

def display_move(pokemon, move):
    print(f"{pokemon} used {move}!")

def subtract_damage(pokemon_hp, damage):
    #return trainer_pokemon_hp - player_pokemon.damage(trainer_pokemon,move)
    return pokemon_hp - damage

def display_hp(team, pokemon):
    return team[pokemon]

def pick_opponent():
    return random.choice(trainer_team)

def check_ending():
    if len(trainer_team) == 0 or len(player_team) == 0:
        if len(trainer_team) == 0:
            print("Trainer is out of usable pokemons")
        else:
            print("You're out of usable pokemons")
        return True
    
def check_if_fainted(pokemon_hp):
    if pokemon_hp <= 0:
        return True
    
def remove(pokemon, team):
#def remove_from_team(pokemon, team):
    print(f"{pokemon} fainted!\n")
    team.remove(pokemon)

###########################################
#############PHASE 1: THE RULES############
###########################################

rules = "Règles du jeu: ...."

player_name = input("What is your name?\n")

print(rules)

###########################################
##########PHASE 2: ASSEMBLE TEAMS##########
###########################################

# there are four pokemons in the player team: 3 they choose in player_pokemons list + 1 random
while len(player_team) < 3:
    prompt_team()

while len(player_team) < 4:
    random_pokemon = random.choice(available_pokemons)
    player_team.add(random_pokemon)

print(f"And your random Pokémon is...")

print(f"{random_pokemon} !!!\n")

# le premier pokémon choisi est le premier à entrer dans l'arène, changer de pokémon coûtera un tour
player_team = list(player_team)
original_team = player_team

player_pokemon = player_team[0]

# there are 10 pokemons in the trainer team
# opponent is picked randomly 
trainer_pokemon = pick_opponent()

###########################################
##############PHASE 3: FIGHT###############
###########################################

# quand les HP d'un pokémon arrivent à zéro, le pokémon sera retiré de de usable_pokémons
usable_pokemons = player_team

# dictionnaire qui contient le niveaux de HP de tous pokémons de l'équipe encore en vie; quand cette valeur totale est égale à zéro, le combat est perdu
player_team_hp = team_hp(player_team)

trainer_team_hp = team_hp(trainer_team)

# nombre de HP du pokémon combattant
trainer_pokemon_hp = trainer_team_hp[trainer_pokemon]

player_pokemon_hp = player_team_hp[player_pokemon]

print(f"First opponent is...")

print(f"{trainer_pokemon} !!!\n")

#print(f"\nWild {trainer_pokemon} appeared!\n")

while len(usable_pokemons) != 0:
    # boucle while 1 = boucle d'entrée et de sortie du combat pour le player
    # entrée = entrée en jeu d'un pokémon du player, soit début de la partie ou remplacement d'un pokémon mort (!= changement d'un pokémon)
    # sortie = plus de pokémons disponibles pour trainer (victoire) ou pour le player (défaite)
    print("(boucle 1)")

    #check_ending()
    # if check_ending() == True:
    #     break

    if len(trainer_team) == 0:
        print("Trainer is out of usable pokemons")
        print("(fin du combat #boucle1)")
        print("YOU WIN")
        exit()
    
    if len(usable_pokemons) < 4:
        print("(changement de pokemon)")
        choice_pokemon = [
        inquirer.List('pokemon',
                        message=f"Choose a Pokémon",
                        choices=player_team,
                    ),
        ]
        choice_pokemon = inquirer.prompt(choice_pokemon)
        player_pokemon = choice_pokemon['pokemon']
        player_pokemon_hp = player_team_hp[player_pokemon]

        print(f"Go! {player_pokemon}!\n")
    
        print(f"(hp player_pokemon {player_pokemon} {player_pokemon_hp})")


    # boucle while 2: phase de combat d'un pokémon
    while player_pokemon_hp > 0:
        
        print("(boucle 2)")

        # à ajouter: choisir quel joueur commence en fonction de la vitesse du pokémon choisi

        action = prompt_action()
        
        if action == 'FIGHT':
            move = prompt_fight()
            display_move(player_pokemon, move)

            damage = player_pokemon.damage(trainer_pokemon,move)

            #print(f"{player_pokemon} used {chosen_move}!")
            
            #print(f"damage {damage}")
            #print(f"formule {player_pokemon.damage(trainer_pokemon,move)}")

            #print(f"(--- hp du trainer_pokemon {trainer_pokemon} avant: {trainer_pokemon_hp})")
            
            #trainer_pokemon_hp = trainer_pokemon_hp - player_pokemon.damage(trainer_pokemon,chosen_move)
            #trainer_pokemon_hp = trainer_pokemon_hp - damage
            # on ne peut pas mettre ça dans une fonction:
            trainer_pokemon_hp = subtract_damage(trainer_pokemon_hp, damage)
            
            #print(f"(--- hp du trainer_pokemon {trainer_pokemon} après: {trainer_pokemon_hp})")

            # remplacement du Pokémon du trainer // s'il lui reste d'autres pokémons, pas besoin de sortir de la boucle 2 car pas d'action du player

            # NOUVEAU: A METTRE EN PLACE SI MARCHE POUR PLAYER
            if check_if_fainted(trainer_pokemon_hp) == True:
                remove(trainer_pokemon, trainer_team)
                if check_ending() == True:
                    break
                else:
                    trainer_pokemon = pick_opponent()
                    trainer_pokemon_hp = trainer_team_hp[trainer_pokemon]
                    print(f"Trainer send {trainer_pokemon} !!!\n")
            else:
                print(f"Trainer's {trainer_pokemon} HP is now {trainer_pokemon_hp}\n")

            
            # if trainer_pokemon_hp <= 0:
            #     print(f"HAUT {trainer_pokemon} fainted!\n")
            #     # à faire: créer équivalent de usable_pokemons for trainer?
            #     trainer_team.remove(trainer_pokemon)
            #     # s'il s'agissait de son dernier pokémon: on retourne dans la boucle 1
            #     # if check_ending == True:
            #     #     break
            #     if len(trainer_team) == 0:
            #         break
            #     # sinon on remplace simplement par un autre Pokémon de sa team sans quitter la boucle de combat du pokémon du player
            #     else:
            #     #if len(trainer_team) < 10:
            #         trainer_pokemon = pick_opponent()
            #         # update HP fight
            #         trainer_pokemon_hp = trainer_team_hp[trainer_pokemon]
            #         print(f"Trainer send {trainer_pokemon} !!!\n")
            #     #break

            # # si Pokémon du player meure // inutile à cet endroit HAUT:
            # if check_faint == True:
            #     kill(player_pokemon, player_team)
            # # if player_pokemon_hp <= 0:
            # #     print(f"{player_pokemon} fainted!\n")
            # #     usable_pokemons.remove(player_pokemon)
            #     if len(usable_pokemons) == 0:
            #         break
            #     else:
            #         # choix à enlever:
            #         choice = input("HAUT Use next POKéMON? (y/n) // JAMAIS AFFICHE")
            #         while choice.lower() != 'y' and choice.lower() != 'n':
            #             choice = input("Use next POKéMON? (y/n)")
            #         if choice == 'y':
            #             break

        if action == 'CHANGE POKéMON':
            player_pokemon = prompt_change()
            player_pokemon_hp = player_team_hp[player_pokemon]

        while action == 'RUN':
            print("You can't run\n")
            action = prompt_action()

        while action == f"{player_pokemon} SUMMARY":
            Console().print(player_pokemon)
            action = prompt_action()

        ################### trainer_pokemon's turn #################

        # ok de faire deux fois appel à variable moves et damage où je dois créer move_trainer et move_player?
        # faire une seule grosse fonction pour attaquer avec display/subtract etc?

        #trainer_pokemon_move = random.choice(trainer_pokemon.moves)
        #print(f"{trainer_pokemon} used {trainer_pokemon_move}")
        
        move = random.choice(trainer_pokemon.moves)
        display_move(trainer_pokemon, move)
        
        damage = trainer_pokemon.damage(player_pokemon,move)

        #print(f"--- hp du player_pokemon {player_pokemon} avant: {player_pokemon_hp}")

        #player_pokemon_hp = player_pokemon_hp - trainer_pokemon.damage(player_pokemon,trainer_pokemon_move)
        
        #player_team_hp[player_pokemon] = player_pokemon_hp

        player_pokemon_hp = subtract_damage(player_pokemon_hp, damage)
        
        #print(f"--- hp du player_pokemon {player_pokemon} après: {player_pokemon_hp}")
        
        ################################################

        # if trainer_pokemon_hp <= 0:
        #     print(f"BAS: {trainer_pokemon} fainted!\n // JAMAIS AFFICHE")
        #     print(trainer_team)
        #     trainer_team.remove(trainer_pokemon)
        #     print(trainer_team)
        #     break

        if check_if_fainted(player_pokemon_hp) == True:
            remove(player_pokemon, player_team)
            if check_ending() == True:
                break
            else:
            #if len(usable_pokemons) != 0:
                choice = input("Use next POKéMON? (y/n)")
                while choice.lower() != 'y' and choice.lower() != 'n':
                    choice = input("Use next POKéMON? (y/n)")
                if choice == 'y':
                    break
                elif choice == 'n':
                    print("You can't escape\n")
            # else:
            #     break
        else:
            print(f"Your {player_pokemon} HP is now {player_pokemon_hp}\n")
        # if player_pokemon_hp <= 0:
        #     print(usable_pokemons)
        #     print(f"{player_pokemon} fainted!\n")
        #     usable_pokemons.remove(player_pokemon)
        #     print(usable_pokemons)

victimes = 10 - len(trainer_team)
print(f"You killed {victimes} Pokémons")
with open('record.txt', 'a') as f:
    f.write(f"{player_name} killed {victimes} Pokémons with team {original_team}\n")
    f.close()