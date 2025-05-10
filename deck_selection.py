import random 
from input_validation import validate_input 

def deck_selection(human_decks, cat_decks):
    
    valid_inputs = list()
    
    for index, deck in enumerate(human_decks): # go through each deck
        # print deck number in list
        print(f'Deck {index + 1}')
        valid_inputs.append(index + 1)
        
        for card_num, card in enumerate(deck):
            print(f'{card_num + 1}: {card}')
        print()
    
    input = validate_input("Choose your deck: ", data_type=int, allowed_values=valid_inputs)
    human_selection = int(input) - 1
    computer_selection = random.choice(cat_decks)
    return human_selection, computer_selection