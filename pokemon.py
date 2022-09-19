from re import A
import pandas
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table
import random
import math
import inquirer

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
        #for targets that have multiple types, the type effectiveness of a move is the product of its effectiveness against each of the types
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
        #for targets that have multiple types, the type effectiveness of a move is the product of its effectiveness against each of the types
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

        print(move.effectiveness(target))
        if move.effectiveness(target) > 2:
            print(("It's super effective!"))
        if move.effectiveness(target) < 1:
            print(("It's not very effective..."))

        return ((((((2 * level * critical) / 5) + 2) * power * attack / defense) / 50) + 2) * STAB * move.effectiveness(target) * nbrandom


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

tackle = Move(name="Tackle", type="Normal", category="Physical", power=35)

vinewhip = Move(name="Vine Whip", type="Grass", category="Special", power=35)

razorleaf = Move(name="Razor Leaf", type="Grass", category="Special", power=55)

solarbeam = Move(name="Solar Beam", type="Grass", category="Special", power=120)

doubleedge = Move(name="Double Edge", type="Normal", category="Physical", power=100)

quickattack = Move(name="Quick Attack", type="Normal", category="Physical", power=40)

rage = Move(name="Rage", type="Normal", category="Physical", power=20)

earthquake = Move(name="Earthquake", type="Ground", category="Physical", power=100)

rockslide = Move(name="Rock Slide", type="Rock", category="Physical", power=75)

bodyslam = Move(name="Body Slam", type="Normal", category="Physical", power=85)

stomp = Move(name="Stomp", type="Normal", category="Physical", power=65)

slash = Move(name="Slash", type="Normal", category="Physical", power=70)

thundershock = Move(name="Thunder Shock", type="Electric", category="Special", power=45)

thunderwave = Move(name="Thunder Wave", type="Electric", category="Physical", power=65)

acid = Move(name="Acid", type="Poison", category="Physical", power=40)

poisonsting = Move(name="Poison Sting", type="Poison", category="Physical", power=15)

constrict = Move(name="Constrict", type="Normal", category="Physical", power=10)

bubblebeam = Move(name="Bubble Beam", type="Water", category="Special", power=65)


#**************************

#*********POKEMONS*********
#**************************

zubat = Pokemon(name="Zubat", type=["Poison", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 35, "Special Attack": 30, "Special Defense": 40, "Speed": 55}, moves=[leechlife, wingattack, bite, megadrain])

slowpoke = Pokemon(name="Slowpoke", type=["Water", "Psychic"], stats={"Health": 90, "Attack": 65, "Defense": 65, "Special Attack": 40, "Special Defense": 40, "Speed": 15}, moves=[headbutt, confusion, watergun, psychic])

bulbasaur = Pokemon(name="Bulbasaur", type=["Grass", "Poison"], stats={"Health": 45, "Attack": 49, "Defense": 49, "Special Attack": 65, "Special Defense": 65, "Speed": 45}, moves=[tackle, vinewhip, razorleaf, solarbeam])

pidgey = Pokemon(name="Pidgey", type=["Normal", "Flying"], stats={"Health": 40, "Attack": 45, "Defense": 40, "Special Attack": 35, "Special Defense": 35, "Speed": 56}, moves=[doubleedge, quickattack, wingattack, rage])

venonat = Pokemon(name="Venonat", type=["Bug", "Poison"], stats={"Health": 60, "Attack": 55, "Defense": 50, "Special Attack": 40, "Special Defense": 40, "Speed": 45}, moves=[psychic, megadrain, doubleedge, tackle])

rhyhorn = Pokemon(name="Rhyhorn", type=["Ground", "Rock"], stats={"Health": 80, "Attack": 85, "Defense": 95, "Special Attack": 30, "Special Defense": 30, "Speed": 25}, moves=[earthquake, rockslide, bodyslam, stomp])

farfetchd = Pokemon(name="Farfetch'd", type=["Normal", "Flying"], stats={"Health": 52, "Attack": 65, "Defense": 55, "Special Attack": 58, "Special Defense": 58, "Speed": 60}, moves=[bodyslam, slash, bodyslam, stomp])

magnemite = Pokemon(name="Magnemite", type=["Electric", "Steel"], stats={"Health": 25, "Attack": 35, "Defense": 70, "Special Attack": 95, "Special Defense": 95, "Speed": 45}, moves=[thundershock, thunderwave, slash, rage])

tentacool = Pokemon(name="Tentacool", type=["Water", "Poison"], stats={"Health": 40, "Attack": 40, "Defense": 35, "Special Attack": 100, "Special Defense": 100, "Speed": 70}, moves=[acid, poisonsting, constrict, bubblebeam])

###########################################
##########NUMERORATION DECK################
###########################################
dicodeck = {}
deck = [zubat, "poupou", "loulou"]
for pokemon in range(len(deck)):
    dicodeck[pokemon] = deck[pokemon]

decknum = [f"{number} {pokemon}" for number,pokemon in enumerate(deck)]
strdeck = "\n".join(decknum)
#print(strdeck)

dicodeck = {pokemon: index for (pokemon, index) in enumerate(deck)}
#print(dicodeck)

dicotest = {chiffre: (deck.index(chiffre)+1) for chiffre in deck}
#print(dicotest)

# convdeck = [str(pokemon) for pokemon in deck]
# print(convdeck)
# strdeck = "\n".join(convdeck)
# print(strdeck)

###########################################
###################GAME####################
###########################################

wild_pokemons = [rhyhorn, magnemite, slowpoke]

my_pokemons = [bulbasaur, farfetchd, zubat, venonat, tentacool, pidgey]

foe = random.choice(wild_pokemons)

print('!!!\n')

print(f"Wild {foe} appeared!\n")

print(f"Go! {my_pokemons[0]}!\n")

# questions = [
#   inquirer.List('your_pokemon',
#                 message="Select your Pokémon",
#                 choices=my_pokemons,
#             ),
# ]
# your_pokemon = answers['your_pokemon']
# answers = inquirer.prompt(questions)

question_1 = [
  inquirer.List('choice',
                message=f"What should {my_pokemons[0]} do?",
                choices=['Fight', 'Pokémons', 'Run'],
            ),
]

answers = inquirer.prompt(question_1)

print(f"Foe {foe} used {random.choice(foe.moves)}\n")

# questions_2 = [
#   inquirer.List('your_choice',
#                 message=f"What should {your_pokemon} do?",
#                 choices=your_pokemon.moves,
#             ),
# ]

# answers = inquirer.prompt(questions_2)


# print(f"{answers['your_pokemon'].upper()} used !")

#wprint("TRAINER CHRISTINA would like to battle!")
#wprint("TRAINER CHRISTINA send out ")