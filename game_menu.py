from updated_user_validation import validate_user_input 

def game_menu(deck, player, cat):
    # prints game options

    option = validate_user_input("Menu:\
        \nOption 1: select card\
        \nOption 2: show your deck\
        \nOption 3: show stats\
        \nSelect option: ", int, [1, 2, 3])
    # 3rd option: print opponent's deck
    # input validation
    
    while option != 1:
        if option == 2:
            print()
            counter = 1
            for card in deck:
                print(f'{counter}: {card}')
                counter += 1
            print()
        elif option == 3:
            print(f"\n{player}\n{cat}\n")
        option = int(input("Select option: "))
        
    selection = validate_user_input(f"Select card 1-{len(deck)}: ", int, 
                                    [deck.index(card) + 1 for card in deck]) - 1 
    print()
    
    return deck[selection]
    
   
        