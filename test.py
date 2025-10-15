from caesar.util.add_ import add_
from caesar.util.delete import delete
from caesar.util.search import search_room
from caesar.util.direct_insert_room import direct_insert_room   
from caesar.util.sort_data import sort_data
from caesar.util.add_more import add_more

count = 1
ht = add_(5, 1, [5])
print("\n----------add--------\n")
print(ht)
print(ht.size)
# print(search_room(ht, 5))
# print(delete(ht, 5))
# print(search_room(ht, 5))
# print()
# count = direct_insert_room(ht, 5, count)
# print(ht)
# print(count)
# print()
# print(sort_data(ht))
print("\n----------add more--------\n")
ht = add_more(ht, 2, [10, 5])
print(ht)
print(ht.size)

