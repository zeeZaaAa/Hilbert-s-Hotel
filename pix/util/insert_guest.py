def insertGuest(db :dict, to_insert :dict):
    if  not isinstance(db, dict):
        return "Error, db must be a dict"
    
    if not isinstance(to_insert, dict):
        return "Error, to_insert must be a list"
    
    if to_insert == {}:
        return db
    
    new_db = {}
    old_keys = list(db.keys())
    old_keys.sort()
    shifter = 0
    for key in old_keys:
        value = db[key]
        key = key + shifter
        while key in to_insert:
            key += 1
            shifter += 1
        new_db[key] = value

    new_db.update(to_insert)
    db = new_db
    return db