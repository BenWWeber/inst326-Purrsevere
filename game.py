import random
import re
from argparse import ArgumentParser

class Game:
    
    def deck_selection(decks):
        for deck in decks:
            # prints current deck index
            print(f'Deck {decks.index(deck)}')
            keys = list(deck.keys())
            
            for key in keys[:2]:
                print(f'(Attack) {key}: {min(deck[key])} - {max(deck[key])}')
            print(f'(Defense) {keys[2]}: {deck[keys[2]]}')
            # add other powerup types
            if keys[3][0] == 'A':
                powerup_type = 'attack stat'
            print(f'(Powerup: {powerup_type}) {keys[3]}: {deck[keys[3]]} \n')
        
        human_selection = int(input("Choose your deck: "))
        return human_selection, random.choice(range(2))
    
    def computer_card_draw(owner_hp, cat_hp, cat_cards, owner_cards):
        """Determines which card the computer (cat) draws. Prioritizes defense
        (if computer can be defeated in one turn), then attack (if owner can be
        defeated in one turn), then either attack or a powerup
        
        Args: 
            owner_hp (int): health points of the owner (player)
            cat_hp (int): health points of the cat (computer)
            cat_cards (dict): dict containing cat's available cards as keys
                            with their effects as values
            owner_cards (dict): dict containing owner's available cards as keys
                            with their effects as values
                            
        Side effects:
            None
    """
        owner_keys = list(owner_cards.keys())
        cat_keys = list(cat_cards.keys())
        atk_1_max = max(cat_cards[cat_keys[0]])
        atk_2_max = max(cat_cards[cat_keys[1]])
        
        #defend when owner's (player) attack can defeat cat (computer)
        for key in range(2):
            if max(owner_cards[owner_keys[key]]) >= cat_hp:
                return cat_keys[2]      
                
        #draw attack card if can defeat owner (player)    
        #chooses strongest possible attack for increased chance of winning 
        if atk_1_max > atk_2_max and atk_1_max >= owner_hp:
            return cat_keys[0]
        if atk_2_max >= owner_hp:
            return cat_keys[1]
    
            
        #choose between attack and powerup, greater chance of attack
        #randomly chooses attack
        percentage = random.choice(range(101))
        #attack 70% of the time
        if percentage >= 30:
            return cat_keys[random.choice(range(2))]
        else:
            return cat_keys[3]
    
    def process_deck(input_file, cat_output_file,owner_output_file,deck_number):
    
        """ Takes the deck number as an input finds it from the card file then 
        writes it to a file"""
        
        try:
            with open(input_file, 'r', encoding="utf8") as file:
                lines = input_file.readlines()
        except FileNotFoundError:
            print(f"Error {input_file} was not found") 
            return
        
        found_deck = False
        deck_data = []
        
        for line in lines:
            line = line.strip()
            
            if line.startwith(str(deck_number) + ':'):
                found_deck = True
                stats = line.split(':')[1].strip().split(',')
                for stat in stats:
                    deck_data.append(stat.strip())
                    
        if not found_deck:
            print(f"Deck {deck_number} not found")
            
            return
        
        cat_stats = {
            'health_points' : deck_data[-2],
            'attack_multiplayer' : deck_data[-1] 
        }
        
        owner_stats = {
            'health_points' : deck_data[-2],
            'attack_multiplayer' : deck_data[-1] 
        }
        
        
        try:
            with open(cat_output_file,'w',encoding="utf8") as cat_file:
                cat_file.write("Cat Stats: \n")
                for key,value in cat_stats.items():
                    cat_file.write(f"{key}:{value}\n")
        except:
            print("Error writing to the cat output file")
            return
        
        try:
            with open(owner_output_file,'w',encoding="utf8") as owner_file:
                owner_file.write("Owner Stats: \n")
                for key,value in owner_stats.items():
                    owner_file.write(f"{key}:{value}\n")
        except:
            print("Error writing to the owner output file")
            return
    
    def resolve_attack(card_accuracy, damage_range, user_multiplier = 1.0, 
                    defender_multiplier = 1.0):
        """
        Resolves an offensive card attack

        Args:
            card_accuracy (int): accuracy of card played
            damage_range (range or tuple): damage range of played card
            user_multiplier (float): multiplier of buffs/weaknesses applied to the 
                user's attack. Defaults to 1.0.
            defender_multiplier (float): multiplier of buffs/weaknesses applied to 
                defender's defense. Defaults to 1.0.
        
        Returns:
            str: If attack hits is true then calculate damage, else it 
                returns false and 0.
                
        Raises:
            ValueError: If the damage_range is neither a tuple or a range
                instance of valid length.

        Side Effects:
            Uses the global random number generator state by calling
            random.randint, which affects subsequent calls to random.
        """
        # determine rng/accuracy of attack 
        rng = random.random() * 100 # 0-99
        if not rng < card_accuracy:
            determine_hit, damage = False, 0
        else:
            determine_hit = True
        
        # determine damage
        if isinstance(damage_range, range):
            min_damage = damage_range.start
            max_damage = damage_range[-1]
            damage = random.randint(min_damage, max_damage)
        if isinstance(damage_range, tuple) and len(damage_range) == 2:
            damage = random.randint(damage_range[0], damage_range[1])
        else:
            raise ValueError("damage_range must be a range or tuple with (min/max)")
        
        # calculate multipliers
        total_multiplier = user_multiplier * defender_multiplier
        damage = int(damage * total_multiplier)
        
        if determine_hit:
            return f"Attack hits! Damage dealt: {damage}"
        else:
            return f"Attack missed! Damage dealt: 0"
        
    if __name__ == "__main__":
        # Attack card with 80% accuracy and damage between 10 and 30
        accuracy = 80
        damage_range = (10, 30)
        attacker_buff = 1.5 # attack buff applied
        defender_debuff = 1.3 # debuff applied

        print(resolve_attack(accuracy, damage_range, attacker_buff, 
            defender_debuff))
        
    def show_deck():
        """ Mock function that will return/show the deck the given deck
        """
        print("Deck: (chosen deck goes here)")
        return 

    def validate_input(user_input, ):
        """ Validates User Input and chooses Card
        
        Args:
            user_input (str): the users input to begin the game
            
        Side Effects:
            prints to the console game info and directions
        
        Returns
            str: if the game has ended
            
        Raises:
            ValueError: if the input is incorrect (ie string instead of int or int
                instead of string)
        """
        print("Welcome to Purrsevere")
        print("Enter 'start' to begin the battle or 'end' to quit.")
        decks = [1,2,3,4]
        while True:
            if user_input.lower() == "end":
                return "Game Ended"
            
            elif user_input.lower() == "start":
                deck_input = int(input("Begin by choosing a deck [1, 2, 3, 4]: "))
                if deck_input in decks:
                    print(f"Deck: {deck_input} chosen")
                    return show_deck()
                else:
                    raise ValueError("Deck does not exist. "
                                     + "Please enter 1, 2 , 3 or 4")
            else:
                raise ValueError("Invalid input, please enter 'start' or 'end'")
        
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