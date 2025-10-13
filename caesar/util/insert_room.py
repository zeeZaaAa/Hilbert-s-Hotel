from caesar.classes.Guest import Guest
from caesar.util.insert_to_dict import insert_to_dict

def insert_room(db: dict, roomnumbers: list, num: int):
    try:
        if not isinstance(db, dict):
            return "Error, db must be a dict"
        
        if not isinstance(roomnumbers, list):
            return "Error, guest_roomnumber must be a list"
        
        new_rooms = {}
        for room in roomnumbers:
            if not isinstance(room, int) or room <= 0:
                return f"Error, invalid room number: {room}"
            result = insert_to_dict(new_rooms, room, Guest(chanel="Force-Add", order=num))
            if result != "success":
                return result
            num += 1
        
        start = 1
        count = 1
        while len(db) != 0:
            if new_rooms.get(start) is None:
                while db.get(count) is None and count <= len(db):
                    start+=1
                    count += 1
                result = insert_to_dict(new_rooms, start, db[count])
                if result != "success":
                    return result
                del db[count]
                count += 1
            start += 1
        
        return new_rooms, num
        
    except Exception as e:
        return f"Error: {str(e)}"