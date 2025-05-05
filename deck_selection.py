import random 

decks = [{'scratch': range(15, 26), 
        'pounce': range(30, 61),
        'hair_raise': 20,
        'A_hiss': 1.2
        },
        {'scrub': range(15, 31),
        'pour': range(30, 56),
        'gloves': 15,
        'A_energy_drink': 1.15
        }]


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
    
selections = deck_selection(decks)
print(selections)