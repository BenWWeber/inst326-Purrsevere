def process_deck(input_file, cat_output_file,owner_output_file,deck_number):
    
    
    """ Takes the deck number as an input finds it from the card file then 
    writes it to a file"""
    
    try:
        with open(input_file, 'r', encoding="utf8") as file:
            lines = input_file.readlines()
    except FileNotFoundError:
        print(f"Error {input_file} was not found") 
        return
    
    found_deck = False
    deck_data = []
    
    for line in lines:
        line = line.strip()
        
        if line.startwith(str(deck_number) + ':'):
            found_deck = True
            stats = line.split(':')[1].strip().split(',')
            for stat in stats:
                deck_data.append(stat.strip())
                
    if not found_deck:
        print(f"Deck {deck_number} not found")
        
        return
    
    cat_stats = {
        'health_points' : deck_data[-2],
        'attack_multiplayer' : deck_data[-1] 
    }
    
    owner_stats = {
        'health_points' : deck_data[-2],
        'attack_multiplayer' : deck_data[-1] 
    }
    
    
    try:
        with open(cat_output_file,'w',encoding="utf8") as cat_file:
            cat_file.write("Cat Stats: \n")
            for key,value in cat_stats.items():
                cat_file.write(f"{key}:{value}\n")
    except:
        print("Error writing to the cat output file")
        return
    
    try:
        with open(owner_output_file,'w',encoding="utf8") as owner_file:
            owner_file.write("Owner Stats: \n")
            for key,value in owner_stats.items():
                owner_file.write(f"{key}:{value}\n")
    except:
        print("Error writing to the owner output file")
        return
        

if __name__ == "__main__":
    # Example usage with sample parameters
    input_file = "samplefile.txt"
    cat_output = "cat_stats.txt"
    owner_output = "owner_stats.txt"
    deck_choice = 1
    process_deck(input_file, cat_output, owner_output, deck_choice)