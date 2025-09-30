from ..classes.Guest import Guest

def createGuests(old_guess: int, new_chanel: list, max_chanel: list):
    if not isinstance(old_guess, int):
        return "Error: old_guess must be only integer"
    
    if not (isinstance(new_chanel, list) and isinstance(max_chanel, list)):
        return "Error: new_chanel and max_chanel must be list"
        
    if len(new_chanel) != len(max_chanel):
        return "Error: chanel and number size doesnt match"
    
    old_guests = []
    new_guests = []
    
    for order in range(1, old_guess+1):
        g = Guest("old", order)
        old_guests.append(g)
    
    for chanel, max in zip(new_chanel, max_chanel):
        if str(chanel) == "old":
            return "Error: chanel cannot name 'old'"
        if not isinstance(max, int):
            return "Error: max_chanel must contain only integers"
        for order in range(1, max+1):
            g = Guest(chanel, order)
            new_guests.append(g)
    return old_guests, new_guests

def get_roomnumberAndguests(db: dict):
    if not isinstance(db, dict):
        return "Error: room data must be only dict"
    roomnumber = list(db.keys())
    guests = list(db.values())
    return roomnumber, guests

    

                
        