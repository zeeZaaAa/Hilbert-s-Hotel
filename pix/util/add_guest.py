def add(db :dict, list_of_guest :list):
    if  not isinstance(db, dict):
        return "Error, db must be a dict"
    
    if not isinstance(list_of_guest, list):
        return "Error, list_of_guest must be a list"

    num_to_shift = len(list_of_guest)
    current_keys = list(db.keys())
    for key in current_keys:
        old_guest = db[key]
        db[key+num_to_shift] = str(old_guest)
        db.pop(key)

    room_num = 1
    for guest in list_of_guest:
        db[room_num] = str(guest)
        room_num+=1
    return db