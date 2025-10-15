from caesar.classes.HashTable import HashTable

def save_to_text_from_list(data: list, filename = "File/roomData.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for k, v in data:
            f.write(f"{k}: {v}\n")
            
def save_to_text_from_hashtable(data: HashTable, filename = "File/roomData.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        item = list(data.items())
        for k, v in item:
            f.write(f"{k}: {v}\n")