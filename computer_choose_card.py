import random

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
    cat_powerups = [card for card in cat_deck if card.type == 'buff'
                    or card.type == 'debuff']
    owner_attacks = [card for card in owner_deck if card.type == 'attack']
    
    #defend when owner's (player) attack can defeat cat (computer)
    for card in owner_attacks:
        if max(card.magnitude) >= cat_hp:
            # select strongest defense card
            
    #draw attack card if can defeat owner (player)    
    #chooses strongest possible attack for increased chance of winning 
    cat_attacks.sort(key=max(cat_attacks.magnitude), reverse=True)
    if max(cat_attacks[0].magnitude) >= owner_hp:
        return cat_attacks[0]
        
    #choose between attack and powerup, greater chance of attack
    #randomly chooses attack
    if random.random() < 0.7:
        return random.choice(cat_attacks)
    else:
        return random.choice(cat_powerups)
        


        