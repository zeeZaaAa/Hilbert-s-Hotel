from caesar.classes.HashTable import HashTable  

def search_room(db: HashTable, roomnumber: int):
    try:
        return str(db.get(roomnumber)) if db.get(roomnumber) is not None else f"Room not found: {roomnumber}"
    except KeyError:
        return f"Room not found: {roomnumber}"
    except Exception as e:
        return f"Error: {str(e)}"
