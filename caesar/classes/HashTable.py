class HashTable:

    def __init__(self, capacity=32):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * self.capacity
        self.delete = object()

    def _hash(self, key):
        return key % self.capacity

    def _probe(self, hash_value, i):
        return (hash_value + i * i) % self.capacity

    def _rehash(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for slot in old_table:
            if slot is not None and slot is not self.delete:
                k, v = slot
                self.insert(k, v)

    def insert(self, key, value):
        if self.size / self.capacity > 0.7:
            self._rehash()

        index = self._hash(key)
        i = 0
        while True:
            new_index = self._probe(index, i)
            slot = self.table[new_index]
            if slot is None or slot is self.delete or slot[0] == key:
                if slot is None or slot is self.delete:
                    self.size += 1
                self.table[new_index] = (key, value)
                return
            i += 1
            if i >= self.capacity:
                raise RuntimeError("Hashtable full (shouldn't happen after rehash)")

    def get(self, key):
        index = self._hash(key)
        i = 0
        while i < self.capacity:
            new_index = self._probe(index, i)
            slot = self.table[new_index]
            if slot is None:
                return None
            if slot is not self.delete and slot[0] == key:
                return slot[1]
            i += 1
        return None

    
    def remove(self, key):
        index = self._hash(key)
        i = 0
        while i < self.capacity:
            new_index = self._probe(index, i)
            slot = self.table[new_index]
            if slot is None:
                return False
            if slot is not self.delete and slot[0] == key:
                self.table[new_index] = self.delete
                self.size -= 1
                if self.capacity > 8 and self.size / self.capacity < 0.2:
                    self._shrink()
                return True
            i += 1
        return False

    def _shrink(self):
        old_table = self.table
        self.capacity = max(8, self.capacity // 2)
        self.table = [None] * self.capacity
        self.size = 0
        for slot in old_table:
            if slot and slot is not self.delete:
                k, v = slot
                self.insert(k, v)
    
    def items(self):
        for slot in self.table:
            if slot and slot is not self.delete:
                k, v = slot
                yield k, v
                
    def pop_any(self):
        for slot in self.table:
            if slot and slot is not self.delete:
                key, value = slot
                self.remove(key)
                return key, value
        return None


    def __repr__(self):
        pairs = [f"{k}: {v}" for slot in self.table if slot and slot is not self.delete for k, v in [slot]]
        return "{" + ", ".join(pairs) + "}"
