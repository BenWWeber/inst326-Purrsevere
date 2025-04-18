import random

def resolve_attack(card_accuracy, damage_range, user_multiplier = 1.0, 
                   defender_multiplier = 1.0):
    """
    Resolves an offensive card attack

    Args:
        card_accuracy (int): accuracy of card played
        damage_range (range or tuple): damage range of played card
        user_multiplier (float): multiplier of buffs/weaknesses applied to the 
            user's attack. Defaults to 1.0.
        defender_multiplier (float): multiplier of buffs/weaknesses applied to 
            defender's defense. Defaults to 1.0.
    
    Returns:
        str: If attack hits is true then calculate damage, else it 
            returns false and 0.
            
    Raises:
        ValueError: If the damage_range is neither a tuple or a range
            instance of valid length.

    Side Effects:
        Uses the global random number generator state by calling
        random.randint, which affects subsequent calls to random.
    """
    # determine rng/accuracy of attack 
    rng = random.random() * 100 # 0-99
    if not rng < card_accuracy:
        determine_hit, damage = False, 0
    else:
        determine_hit = True
    
    # determine damage
    if isinstance(damage_range, range):
        min_damage = damage_range.start
        max_damage = damage_range[-1]
        damage = random.randint(min_damage, max_damage)
    if isinstance(damage_range, tuple) and len(damage_range) == 2:
        damage = random.randint(damage_range[0], damage_range[1])
    else:
        raise ValueError("damage_range must be a range or tuple with (min/max)")
    
    # calculate multipliers
    total_multiplier = user_multiplier * defender_multiplier
    damage = int(damage * total_multiplier)
    
    if determine_hit:
        return f"Attack hits! Damage dealt: {damage}"
    else:
        return f"Attack missed! Damage dealt: 0"
    
if __name__ == "__main__":
    # Attack card with 80% accuracy and damage between 10 and 30
    accuracy = 80
    damage_range = (10, 30)
    attacker_buff = 1.5 # attack buff applied
    defender_debuff = 1.3 # debuff applied

    print(resolve_attack(accuracy, damage_range, attacker_buff, 
        defender_debuff))