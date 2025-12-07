class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)

        for pair in self.table[key_hash]:
            if pair[0] == key:
                pair[1] = value
                return

        self.table[key_hash].append([key, value])

    def get(self, key):
        key_hash = self.hash_function(key)

        for pair in self.table[key_hash]:
            if pair[0] == key:
                return pair[1]

        return None

    def delete(self, key):
        key_hash = self.hash_function(key)

        for i, pair in enumerate(self.table[key_hash]):
            if pair[0] == key:
                del self.table[key_hash][i]
                return True  # успішно видалено

        return False  # ключ не знайдено


# Тестування
H = HashTable(5)

H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(f"Banana value: {H.get('banana')}")  # 30

# Перевірка видалення
deleted = H.delete("banana")
print(f"Banana deleted: {deleted}")       # True
print(f"Banana value: {H.get('banana')}") # None