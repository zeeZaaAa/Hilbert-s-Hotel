def add(db :dict, list_of_guest :list):
    if  not isinstance(db, dict):
        return "Error, db must be a dict"
    
    if not isinstance(list_of_guest, list):
        return "Error, list_of_guest must be a list"

    num_to_shift = len(list_of_guest)
    current_keys = list(db.keys())
    newdb = {}
    # shift old guests
    for key in current_keys:
        old_guest = db[key]
        newdb[key+num_to_shift] = old_guest

    # add new guests
    room_num = 1
    while len(list_of_guest) != 0:
        newdb[room_num] = list_of_guest.pop()
        room_num+=1
    return newdb
