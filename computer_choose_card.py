import random

#2 attack cards, 1 defense card, 1 power up
cat_available_cards = {'scratch': range(15, 26), 
                       'pounce': range(30, 61),
                       'hair_raise': 20,
                       'A_hiss': 1.2
                    }
owner_available_cards = {'scrub': range(15, 31),
                        'pour': range(30, 56),
                        'gloves': 15,
                        'A_energy_drink': 1.15
                    }
owner_hp = 100
cat_hp = 100

def computer_card_draw(owner_hp, cat_hp, cat_cards, owner_cards):
    """Determines which card the computer (cat) draws. Prioritizes defense
    (if computer can be defeated in one turn), then attack (if owner can be
    defeated in one turn), then either attack or a powerup
    
    Args: 
        owner_hp (int): health points of the owner (player)
        cat_hp (int): health points of the cat (computer)
        cat_cards (dict): dict containing cat's available cards as keys
                        with their effects as values
        owner_cards (dict): dict containing owner's available cards as keys
                        with their effects as values
                        
    Side effects:
        None
"""
    owner_keys = list(owner_cards.keys())
    cat_keys = list(cat_cards.keys())
    atk_1_max = max(cat_cards[cat_keys[0]])
    atk_2_max = max(cat_cards[cat_keys[1]])
    
    #defend when owner's (player) attack can defeat cat (computer)
    for key in range(2):
        if max(owner_cards[owner_keys[key]]) >= cat_hp:
            return cat_keys[2]      
            
    #draw attack card if can defeat owner (player)    
    #chooses strongest possible attack for increased chance of winning 
    if atk_1_max > atk_2_max and atk_1_max >= owner_hp:
        return cat_keys[0]
    if atk_2_max >= owner_hp:
        return cat_keys[1]
 
        
    #choose between attack and powerup, greater chance of attack
    #randomly chooses attack
    percentage = random.choice(range(101))
    #attack 70% of the time
    if percentage >= 30:
        return cat_keys[random.choice(range(2))]
    else:
        return cat_keys[3]
        

computer_card_draw(owner_hp, cat_hp, cat_available_cards, 
                   owner_available_cards)
        