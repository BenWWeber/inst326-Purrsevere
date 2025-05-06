import random
import re
from argparse import ArgumentParser


class Card:
    def __init__(self, name, description, type_, magnitude, power_level, accuracy):
        self.name = name
        self.description = description
        self.type = type_
        self.magnitude = magnitude
        self.power_level = power_level
        self.accuracy = accuracy

    def __repr__(self):
        return (
            f'Card Name: {self.name}, Description: {self.description}, '
            f'Type: {self.type}, Magnitude: {self.magnitude}, '
            f'Power Level: {self.power_level}, Accuracy: {self.accuracy}'
        )
    
    def __str__(self):
        
        match self.type:
            case 'attack':
                return (f'{self.name}: {self.description}. does '
                + f'{self.magnitude[0]} to {self.magnitude[1]} damage with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'defence':
                return (f'{self.name}: {self.description}. adds '
                + f'{self.magnitude} defence with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'attack buff':
                return (f'{self.name}: {self.description}. add a '
                + f'{int(self.magnitude*100)}% buff to your attack with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'attack debuff':
                return (f'{self.name}: {self.description}. add a '
                + f"{int(self.magnitude*100)}% debuff to your cats' attack with "
                + f'{int(self.accuracy*100)}% accuracy')
            case 'defence buff':
                return (f'{self.name}: {self.description}. add a '
                + f'{int(self.magnitude*100)}% buff to your defence with '
                + f'{int(self.accuracy*100)}% accuracy')
            case 'defence debuff':
                return (f'{self.name}: {self.description}. add a '
                + f"{int(self.magnitude*100)}% debuff to your cats' defence with "
                + f'{int(self.accuracy*100)}% accuracy')


class Player:
    def __init__(self, name="Player", health=100):
        self.name = name
        self.health = health
        self.attack_multiplier = 1.0
        self.defense_multiplier = 1.0

    def change_stat(self, stat, multiplier):
        if stat == 'attack':
            self.attack_multiplier *= multiplier
        elif stat == 'defense':
            self.defense_multiplier *= multiplier
        else:
            raise ValueError("Invalid stat; choose 'attack' or 'defense'")

    def is_defeated(self):
        return self.health <= 0

    def __str__(self):
        return (
            f"{self.name}: HP={self.health}, AtkMult={self.attack_multiplier}, "
            f"DefMult={self.defense_multiplier}"
        )



def deck_selection(player_decks, cat_decks):
    # decks = list of decks

    for idx, deck in enumerate(player_decks): # go through each deck
        # print deck number in list
        print(f'Deck {idx + 1}')
        
        for card in deck:
            print(f'\t{card}')
        # not needed each deck is now list of Cards
        # # keys = list(deck.keys())

        # # show two attacks
        # for key in keys[:2]:
        #     print(f'(Attack) {key}: {min(deck[key])} - {max(deck[key])}')

        # # defense
        # def_key = keys[2]
        # print(f'(Defense) {def_key}: {deck[def_key]}')

        # # powerup type
        # powerup_type = 'attack stat' if keys[3][0] == 'A' else 'unknown'
        # print(f'(Powerup: {powerup_type}) {keys[3]}: {deck[keys[3]]}\n')

    human_selection = int(input("Choose your deck: "))
    computer_selection = random.randint(0, len(cat_decks) - 1)
    return player_decks[human_selection - 1], cat_decks[computer_selection]

def computer_card_draw(owner_hp, cat_hp, cat_cards, owner_cards):
    owner_keys = list(owner_cards.keys())
    cat_keys = list(cat_cards.keys())
    atk_1_max = max(cat_cards[cat_keys[0]])
    atk_2_max = max(cat_cards[cat_keys[1]])

    # defend if owner can kill cat
    for i in range(2):
        if max(owner_cards[owner_keys[i]]) >= cat_hp:
            return cat_keys[2]

    # attack if can kill owner
    if atk_1_max > atk_2_max and atk_1_max >= owner_hp:
        return cat_keys[0]
    if atk_2_max >= owner_hp:
        return cat_keys[1]

    # otherwise random: 70% attack
    if random.random() < 0.7:
        return random.choice(cat_keys[:2])
    return cat_keys[3]

def process_deck(input_file, cat_output_file, owner_output_file, deck_number):
    try:
        with open(input_file, 'r', encoding="utf8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: {input_file} was not found")
        return

    found_deck = False
    deck_data = []
    for line in lines:
        line = line.strip()
        if line.startswith(str(deck_number) + ':'):
            found_deck = True
            stats = line.split(':', 1)[1].split(',')
            deck_data = [s.strip() for s in stats]
            break

    if not found_deck:
        print(f"Deck {deck_number} not found")
        return

    # assume last two entries are health and multiplier
    hp = deck_data[-2]
    amp = deck_data[-1]
    cat_stats = {'health_points': hp, 'attack_multiplier': amp}
    owner_stats = {'health_points': hp, 'attack_multiplier': amp}

    try:
        with open(cat_output_file, 'w', encoding="utf8") as cat_file:
            cat_file.write("Cat Stats:\n")
            for k, v in cat_stats.items():
                cat_file.write(f"{k}:{v}\n")
    except IOError:
        print("Error writing to the cat output file")
        return

    try:
        with open(owner_output_file, 'w', encoding="utf8") as owner_file:
            owner_file.write("Owner Stats:\n")
            for k, v in owner_stats.items():
                owner_file.write(f"{k}:{v}\n")
    except IOError:
        print("Error writing to the owner output file")
        return

def resolve_attack(card_accuracy, damage_range, user_multiplier=1.0, defender_multiplier=1.0):
    rng = random.random() * 100
    if rng >= card_accuracy:
        return False, 0

    if isinstance(damage_range, range):
        damage = random.randint(damage_range.start, damage_range[-1])
    elif isinstance(damage_range, tuple) and len(damage_range) == 2:
        damage = random.randint(damage_range[0], damage_range[1])
    else:
        raise ValueError("damage_range must be a range or a tuple of length 2")

    damage = int(damage * user_multiplier * defender_multiplier)
    return True, damage

def show_deck():
    print("Deck: (chosen deck goes here)")

def validate_input(user_input):
    print("Welcome to Purrsevere")
    print("Enter 'start' to begin the battle or 'end' to quit.")
    decks = [1, 2, 3, 4]

    while True:
        cmd = user_input.lower()
        if cmd == 'end':
            return "Game Ended"
        if cmd == 'start':
            choice = int(input("Begin by choosing a deck [1-4]: "))
            if choice in decks:
                print(f"Deck: {choice} chosen")
                return show_deck()
            raise ValueError("Deck does not exist. Please enter 1, 2, 3, or 4")
        raise ValueError("Invalid input, please enter 'start' or 'end'")

def apply_card_effect(card, user, target):
    if card.type == 'attack':
        hit, dmg = resolve_attack(
            card.accuracy,
            card.magnitude,
            user.attack_multiplier,
            target.defense_multiplier
        )
        if hit:
            target.health -= dmg
            print(f"{user.name}'s {card.name} hits for {dmg} damage!")
        else:
            print(f"{user.name}'s {card.name} missed!")
    elif card.type == 'defense':
        target.change_stat('defense', card.magnitude)
        print(f"{target.name} gains defense x{card.magnitude}")
    elif card.type == 'buff':
        user.change_stat('attack', card.magnitude)
        print(f"{user.name}'s attack buff x{card.magnitude}")
    elif card.type == 'debuff':
        target.change_stat('attack', 1.0 / card.magnitude)
        print(f"{target.name}'s attack debuffed /{card.magnitude}")
    else:
        print(f"Unknown card type: {card.type}")

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
                    mag = (int(mag[0]),int(mag[1]))
                                        
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

if __name__ == "__main__":
    print('Welcome to Purrsevere!\n')

    print('''_._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-\n''')
    
    print('Start by choosing a deck:')
    
    # make 3 player decks and 3 cat decks
    player_decks = list()
    while len(player_decks) < 5:
        player_decks.append(make_deck('player_cards.txt', 6, 15))

    cat_decks = list()
    while len(cat_decks) < 5:
        cat_decks.append(make_deck('player_cards.txt', 6, 15)) # change path later
    
    player_deck, cat_deck = deck_selection(player_decks, cat_decks)

    print('chosen deck:')
    for card in player_deck:
        print(f'\t{card}')
    