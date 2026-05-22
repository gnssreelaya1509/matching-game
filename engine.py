import random

class MemoryEngine:
    def __init__(self, grid_size=4):
        self.grid_size = grid_size
        self.cards = self._generate_cards()
        self.matched_indices = set()

    def _generate_cards(self):
        # Create pairs: 1,1, 2,2, 3,3, 4,4, 5,5, 6,6, 7,7, 8,8
        pairs = list(range(1, (self.grid_size * self.grid_size // 2) + 1)) * 2
        random.shuffle(pairs)
        return pairs

    def check_match(self, idx1, idx2):
        if self.cards[idx1] == self.cards[idx2]:
            self.matched_indices.add(idx1)
            self.matched_indices.add(idx2)
            return True
        return False