from caesar.classes.HashTable import HashTable
from caesar.util.calculate_roomnumber import calculate_roomnumber
from caesar.classes.Guest import Guest  

def add_more(old_guest :HashTable, chanel: int, nums_of_new_guest :list):    
    db = HashTable()
    
    size = old_guest.size
    max_num_of_new_guest = max(nums_of_new_guest) if len(nums_of_new_guest) > 0 else 0
    max_of_all = max(size, max_num_of_new_guest)

    for diag in range(chanel + max_of_all+1):
        for r in range(diag + 1):
            c = diag - r
            if r == 0 and c < size:
                # print(f'old: {calculate_roomnumber(r,c)}')
                # print(r,c)
                db.insert(calculate_roomnumber(r,c), old_guest.pop_any()[1])
            elif r <= chanel and c < nums_of_new_guest[r-1] and r != 0:
                # print(f'new: {calculate_roomnumber(r,c)}')
                # print(r,c)
                db.insert(calculate_roomnumber(r,c), Guest(chanel=r, order=c+1))
    return db