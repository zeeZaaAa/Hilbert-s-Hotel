from caesar.classes.Guest import Guest
from caesar.classes.HashTable import HashTable

def direct_insert_room(old_guest :HashTable, roomnumber: int, count: int):
    if old_guest.get(roomnumber) is not None:
            return f"Error, room {roomnumber} is not occupied"   
    old_guest.insert(roomnumber, Guest(chanel="Force-Add", order=count))
    count+=1
    return count