import random 

def deck_selection(human_decks, cat_decks):
    for index, deck in enumerate(human_decks): # go through each deck
            # print deck number in list
        print(f'Deck {index + 1}')
        for card in deck:
            print(card)

    human_selection = int(input("Choose your deck: ") - 1)
    computer_selection = random.choice(cat_decks)
    return human_selection, computer_selection