import random 

def deck_selection(decks):
    for index, deck in enumerate(decks): # go through each deck
            # print deck number in list
        print(f'Deck {deck + 1}')
        for card in deck:
            print(card)

        user_input = int(input("Choose your deck: ") - 1)
        # input validation
        human_selection = decks.pop(user_input)
        computer_selection = random.choice(decks)
        return human_selection, computer_selection