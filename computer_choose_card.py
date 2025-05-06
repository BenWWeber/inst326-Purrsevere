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
    cat_attacks.sort(key=max(cat_attacks.magnitude), reverse=True)
    if max(cat_attacks[0].magnitude) >= owner_hp:
        return cat_attacks[0]
        
    #choose between attack and powerup, greater chance of attack
    #randomly chooses attack
    if random.random() < 0.7:
        return random.choice(cat_attacks)
    else:
        return random.choice(cat_powerups)
        


        