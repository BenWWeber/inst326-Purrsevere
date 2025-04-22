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
                raise ValueError("Deck does not exist. Please enter 1, 2 , 3 or 4")
        else:
            raise ValueError("Invalid input, please enter 'start' or 'end'")
        
        
        
if __name__ == "__main__":
    user_input = "start"
    # user_input = "end"
    
    print(validate_input(user_input))