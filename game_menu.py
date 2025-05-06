def game_menu(deck):
    # prints game options

    option = int(input("Menu:\
        \nOption 1: select card\
        \nOption 2: print your deck\
        \nSelect option: "))
    # 3rd option: print opponent's deck
    # input validation
    
    while option != 1:
        if option == 2:
            for card in deck:
                print(card) 
        option = int(input("Select option: "))
    selection = int(input(f"Select card 1-{len(deck)}: ") - 1)  
    
    return deck[selection]
    
   
        