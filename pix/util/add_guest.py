# from caesar.util.insert_to_dict import insert_to_dict
# from caesar.classes.HashTable import HashTable

# def add(db :HashTable, chanel: list, list_of_guest: list):
#     if  not isinstance(db, HashTable):
#         return "Error, db must be a HashTable"
    
#     if not isinstance(list_of_guest, list):
#         return "Error, list_of_guest must be a list"
    
#     for diag in range()


    # int(((n + m-1) * (n + m)) / 2 + m)
    # num_to_shift = len(list_of_guest)
    # current_keys = list(db.keys())
    # newdb = {}
    # # shift old guests
    # for key in current_keys:
    #     old_guest = db[key]
    #     result = insert_to_dict(newdb, key+num_to_shift, old_guest)
    #     if result != "success":
    #         return result

    # # add new guests
    # room_num = 1
    # while len(list_of_guest) != 0:
    #     result = insert_to_dict(newdb, room_num, list_of_guest.pop())
    #     if result != "success":
    #         return result
    #     room_num+=1
    # return newdb
