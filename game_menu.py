def game_menu(deck, player, cat):
    # prints game options

    option = int(input("Menu:\
        \nOption 1: select card\
        \nOption 2: show your deck\
        \nOption 3: show stats\
        \nSelect option: "))
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
    selection = int(input(f"Select card 1-{len(deck)}: ")) - 1 
    
    return deck[selection]
    
   
        