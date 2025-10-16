from caesar.classes.HashTable import HashTable
from caesar.util.calculate_roomnumber import calculate_roomnumber
from caesar.classes.Guest import Guest  

def add_(old_guest :int, chanel: int, nums_of_new_guest :list):    
    db = HashTable()
    
    max_num_of_new_guest = max(nums_of_new_guest) if len(nums_of_new_guest) > 0 else 0
    max_of_all = max(old_guest, max_num_of_new_guest)
    
    for diag in range(chanel + max_of_all+1):
        for r in range(diag + 1):
            c = diag - r
            if r >= chanel + 1:
                break
            if r == 0 and c < old_guest:
                # print(f'old: {calculate_roomnumber(r,c)}')
                # print(r,c)
                db.insert(calculate_roomnumber(r,c), Guest(chanel="old", order=c+1))
            elif r <= chanel and c < nums_of_new_guest[r-1] and r != 0:
                # print(f'new: {calculate_roomnumber(r,c)}')
                # print(r,c)
                db.insert(calculate_roomnumber(r,c), Guest(chanel=r, order=c+1))
    return db
  