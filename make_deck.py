import re
import random

# info on cards: 
# - attack, defence, buff, debuff
# - all have accuracy and strength points
# 
# damage cards' magnitude comes in tuples with min/max
# defence cards' magnitude is just one number
# buff and debuff cards' magnitude come in %

# card class
class Card():
    def __init__(self, name, description, type, magnitude, power_level, accuracy):
        self.name = name
        self.description = description
        self.type = type
        self.magnitude = magnitude
        self.power_level = power_level
        self.accuracy = accuracy
        
    def __str__(self):
        return (f'Card Name: {self.name}, '
                + f'Description: {self.description}, '
                + f'Type: {self.type}, '
                + f'Magnitude: {self.magnitude}, '
                + f'Power Level: {self.power_level}, '
                + f'Accuracy: {self.accuracy}')
    
# make_deck description:
# Creates multiple decks at the beginning of the game that the user can choose 
# from. Chooses cards with assigned strength points. The sum of these values 
# shoud not go higher than a specified max power level. Every deck should have 
# at least one attack, one defence, and one buff/debuff card.
# 
# The algorithm will need: 
#  - Card names, descriptions, and stats, which will be pulled from and created 
#        algorithmically from a data file
#  - Specified numbers of cards to put in deck
#  - Max power level of deck

# deck function (4/22 deliverable)
def make_deck(path, max_count, max_power):
    deck = list()
    power = 0
    attacks = list()
    defences = list()
    buffs = list()

    # read in all the player cards and organize them by type
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            card = re.search('(?P<name>[^;]+);(?P<description>[^;]+);'
                              +'(?P<type>[^;]+);(?P<magnitude>[^;]+);'
                              +'(?P<power_level>[^;]+);(?P<accuracy>[^\n]+)',
                            line)
            
            match card.group('type'):
                case 'attack':
                    
                    mag = card.group('magnitude').split(',')
                    mag = {int(mag[0]),int(mag[1])}
                                        
                    attacks.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        mag,
                                        float(card.group('power_level')),
                                        float(card.group('accuracy')),))
                case 'defence':
                    defences.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        float(card.group('magnitude')),
                                        float(card.group('power_level')),
                                        float(card.group('accuracy')),))
                case 'buff' | 'debuff':
                    buffs.append(Card(card.group('name'),
                                        card.group('description'),
                                        card.group('type'),
                                        float(card.group('magnitude')),
                                        float(card.group('power_level')),
                                        float(card.group('accuracy')),))

    # add one random attack and remove from list
    current_card = attacks.pop(random.randint(0, len(attacks) - 1))
    power += current_card.power_level
    deck.append(current_card)
    
    # add one random defence and remove from list
    current_card = defences.pop(random.randint(0, len(defences) - 1))
    power += current_card.power_level
    deck.append(current_card)
    
    # add one random buff/debuff and remove from list
    current_card = buffs.pop(random.randint(0, len(buffs) - 1))
    power += current_card.power_level
    deck.append(current_card)
    
    # put together the card lists
    remaining_cards = attacks + defences + buffs
    
    # sort by power level, highest to lowest
    remaining_cards.sort(key=lambda s: s.power_level, reverse=True)
    
    # add cards until at max power or max card count
    while max_count > len(deck) and remaining_cards:
        
        # remove all cards too strong to fit in the deck
        while remaining_cards and remaining_cards[0].power_level > (max_power - power):
            remaining_cards.pop(0)

        if not remaining_cards:
            break
        
        # select card, if last card in the deck add the strongest remaining card
        if max_count == len(deck) + 1:
            
            strongest_cards = [remaining_cards.pop(0)]
            for card in remaining_cards:
                if card.power_level == strongest_cards[0].power_level:
                    strongest_cards.append(card)
            
            current_card = strongest_cards.pop(random.randint(0, len(strongest_cards) - 1))
            power += current_card.power_level
            deck.append(current_card)
        else:
            current_card = remaining_cards.pop(random.randint(0, len(remaining_cards) - 1))
            power += current_card.power_level
            deck.append(current_card)
        
    return deck

# for testing
if __name__ == "__main__":

    # make 5 decks with max 6 cards and max power level of 15
    decks = list()
    while len(decks) < 5:
        decks.append(make_deck('player_cards.txt', 6, 15))
        
    # print out the decks
    for deck in decks:
        print(f'Deck {decks.index(deck) + 1}:')
        lvl = 0
        for card in deck:
            print(f'\t{card}')
            lvl += card.power_level
            
        print(f'\tTotal deck power level: {lvl}\n')
            
    
    
            
            


    