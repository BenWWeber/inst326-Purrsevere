import re


# Creates multiple decks at the beginning of the game that the user can choose 
# from. Chooses x attack cards, y defense cards, z buff/weakness cards, each 
# with assigned strength points. Cannot have >1 strong card in each category. 
# Each deck is assigned a total strength points value, sum of chosen cards 
# cannot exceed this value. 
# 
# The algorithm will need: 
#  - Card names, descriptions, and stats, which will be pulled from and created 
#        algorithmically from a data file
#  - Specified numbers of cards to put in deck
#  - Max power level of decks



# cards: 
# - attack, defence, buff, debuff
# - all have accuracy and strength points
# 
# damage cards damage come in ranges or tuples with min/max
# defence cards probably just one number
# buff and debuff come in %
#
# every deck should have at least one attack, one defence, and one buff/debuff
# not sure how many cards in a deck, probably 4-5

# deck class (not sure we need this over just lists of cards)
class Deck():
    def __init__(self):
        self.cards = list()

# card class
class Card():
    def __init__(self, name, description, type, magnitude, power_level, accuracy):
        self.name = name
        self.description = description
        self.type = type
        self.magnitude = magnitude
        self.power_level = power_level
        self.accuracy = accuracy


# deck function (4/18 deliverable)
def make_deck(path):
    attacks = list()
    defences = list()
    buffs = list()
    debuffs = list()

    # read in all the player cards and organize them by type
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            card = re.search('?P<name>[^;]+);(?P<description>[^;]+);'
                              +'(?P<type>[^;]+);(?P<magnitude>[^;]+);'
                              +'(?P<power_level>[^;]+);(?P<accuracy>[^\n]+',
                            line)
            
            match card.group('type'):
                case 'attack':
                    attacks.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        card.group('magnitude'),
                                        card.group('power_level'),
                                        card.group('accuracy'),))
                case 'defence':
                    defences.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        card.group('magnitude'),
                                        card.group('power_level'),
                                        card.group('accuracy'),))
                case 'buff':
                    buffs.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        card.group('magnitude'),
                                        card.group('power_level'),
                                        card.group('accuracy'),))
                case 'debuff':
                    debuffs.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        card.group('magnitude'),
                                        card.group('power_level'),
                                        card.group('accuracy'),))



    