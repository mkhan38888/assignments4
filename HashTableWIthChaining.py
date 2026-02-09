import random
from typing import Any, List, Tuple, Optional

class HashTableChaining:
    """
    Hash table with separate chaining + universal hashing.
    Supports: insert, search, delete
    Includes dynamic resizing to keep load factor bounded.
    """

    def __init__(self, initial_capacity: int = 8, max_load: float = 0.75):
        if initial_capacity < 1:
            initial_capacity = 1
        self.m = self._next_power_of_two(initial_capacity)
        self.max_load = max_load
        self.n = 0  # number of key-value pairs
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.m)]

        self.p = 2147483647
        self._pick_universal_params()

    def _next_power_of_two(self, x: int) -> int:
        p = 1
        while p < x:
            p <<= 1
        return p

    def _pick_universal_params(self) -> None:
        # Choose a and b uniformly at random
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

    def _key_to_int(self, key: Any) -> int:
        """
        Convert arbitrary key to a non-negative int.
        Using Python's hash is fine for in-memory use (changes between runs).
        """
        return hash(key) & 0x7fffffff  # make non-negative 31-bit

    def _hash(self, key: Any) -> int:
        k = self._key_to_int(key)
        return ((self.a * k + self.b) % self.p) % self.m

    def _resize(self, new_capacity: int) -> None:
        old_items = []
        for bucket in self.table:
            old_items.extend(bucket)

        self.m = self._next_power_of_two(new_capacity)
        self.table = [[] for _ in range(self.m)]
        self.n = 0
        self._pick_universal_params()  # re-randomize hash function

        for k, v in old_items:
            self.insert(k, v)

    def insert(self, key: Any, value: Any) -> None:
        # Resize if load factor too high
        if (self.n + 1) / self.m > self.max_load:
            self._resize(self.m * 2)

        idx = self._hash(key)
        bucket = self.table[idx]

        # If key exists, update
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Otherwise append
        bucket.append((key, value))
        self.n += 1

    def search(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        bucket = self.table[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        bucket = self.table[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.n -= 1

                # Optional: shrink if too empty (keeps memory reasonable)
                if self.m > 8 and self.n / self.m < 0.20:
                    self._resize(self.m // 2)
                return True
        return False

    def load_factor(self) -> float:
        return self.n / self.m


if __name__ == "__main__":
    ht = HashTableChaining(initial_capacity=4, max_load=0.75)

    print("Initial load factor:", ht.load_factor())

    # Insert
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    ht.insert("orange", 30)
    print("Search apple:", ht.search("apple"))     # 10
    print("Search banana:", ht.search("banana"))   # 20
    print("Search missing:", ht.search("grape"))   # None

    # Update existing key
    ht.insert("apple", 99)
    print("Search apple after update:", ht.search("apple"))  # 99

    # Delete
    print("Delete banana:", ht.delete("banana"))   # True
    print("Search banana after delete:", ht.search("banana")) # None
    print("Delete banana again:", ht.delete("banana"))        # False

    print("Final load factor:", ht.load_factor())

    # Stress test resizing
    for i in range(100):
        ht.insert(i, i*i)

    ok = True
    for i in range(100):
        if ht.search(i) != i*i:
            ok = False
            break

    print("Resizing test passed:", ok)
    print("Load factor after inserts:", ht.load_factor())
