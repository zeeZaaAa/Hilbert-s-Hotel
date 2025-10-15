from caesar.classes.HashTable import HashTable

def delete(db: HashTable, roomnumber: int):
    try:
        return "success" if db.remove(roomnumber) else f"Error, room {roomnumber} not found"
    except Exception as e:
        return f"Error: {str(e)}"