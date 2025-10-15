from caesar.classes.HashTable import HashTable

def save_to_text_from_list(data: list, filename="File/roomData.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        text = "\n".join(f"{k}: {v}" for k, v in data)
        f.write(text)


def save_to_text_from_hashtable(data: HashTable, filename="File/roomData.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        text = "\n".join(f"{k}: {v}" for k, v in data.items())
        f.write(text)
