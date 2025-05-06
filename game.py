import random
import re
from argparse import ArgumentParser
from deck_selection import deck_selection
from make_deck import make_deck, Card
from game_menu import game_menu

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
        if self.health <= 0:
            return True
        else:
            return False

    def __str__(self):
        return (
            f"{self.name}: HP={self.health}, AtkMult={self.attack_multiplier}, "
            f"DefMult={self.defense_multiplier}"
        )


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
    card_accuracy *= 100
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

def show_deck(deck, name=''):
    print(f"Deck{name}:")
    for card in deck:
        print(f'\t{card}')

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
                return show_deck(decks)
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
            print(f"{user.name}'s {card.name} hits for {dmg} damage! "
                + f"{target.name} has {target.health} health left.")
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

def computer_card_draw(owner_hp, cat_hp, cat_deck, owner_deck):
    """Determines which card the computer (cat) draws. Prioritizes defense
    (if computer can be defeated in one turn), then attack (if owner can be
    defeated in one turn), then either attack or a powerup
    
    Args: 
        owner_hp (int): health points of the owner (player)
        cat_hp (int): health points of the cat (computer)
        cat_cards (list): list of cat's card objects
        owner_cards (list): list of owner's card objects
                        
    Side effects:
        None
        
    Returns:
        card object
"""
    cat_attacks = [card for card in cat_deck if card.type == 'attack']
    cat_powerups = [card for card in cat_deck if card.type[:-4] == 'buff']
    owner_attacks = [card for card in owner_deck if card.type == 'attack']
    
    #defend when owner's (player) attack can defeat cat (computer)
    cat_defense = [card for card in cat_powerups if card.type == 'defense buff']
    if len(cat_defense) > 0:
        for attack in owner_attacks:
            if max(attack.magnitude) >= cat_hp:
                cat_defense.sort(key=max(cat_defense.magnitude), reverse=True)
                return cat_defense[0]
            
    #draw attack card if can defeat owner (player)    
    #chooses strongest possible attack for increased chance of winning 
    cat_attacks.sort(key=lambda c: max(c.magnitude), reverse=True)
    if max(cat_attacks[0].magnitude) >= owner_hp:
        return cat_attacks[0]
        
    #choose between attack and powerup, greater chance of attack
    #randomly chooses attack
    if random.random() < 0.7:
        return random.choice(cat_attacks)
    else:
        return random.choice(cat_powerups)

def print_menu(player_deck):
    print('game menu goes here')

if __name__ == "__main__":
    '''
    
    ASCII art found at https://www.asciiart.eu/animals/cats
    '''
    print('Welcome to Purrsevere!\n')

    print('''_._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-\n''')
    
    print('Start by choosing a deck:')
    
    # make 3 player decks and 3 cat decks
    player_decks = list()
    while len(player_decks) < 3:
        player_decks.append(make_deck('player_cards.txt', 6, 15))

    cat_decks = list()
    while len(cat_decks) < 3:
        cat_decks.append(make_deck('cat_cards.txt', 6, 15))
    
    player_deck, cat_deck = deck_selection(player_decks, cat_decks)
    player_deck = player_decks[player_deck]
    
    player = Player()
    cat = Player("Cat")
    
    while not cat.is_defeated():
        card = game_menu(player_deck)
        apply_card_effect(card, player, cat)
        computerTurn = computer_card_draw(player.health, cat.health, 
                                          cat_deck, player_deck)
        apply_card_effect(computerTurn, cat, player)
        
        if cat.is_defeated():
            print("You win!")
            break
            
        if player.is_defeated():
            print("Cat wins!")
            break
    