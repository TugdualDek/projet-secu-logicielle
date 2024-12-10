import itertools
import string
from abc import abstractmethod
from base_module import BaseModule

class Module(BaseModule):
    @abstractmethod
    def generate_password_combinations(self, base_word: str, max_length: int = 8):
        chars = string.ascii_letters + string.digits + string.punctuation
        variations = [
            base_word,
            base_word + "123",
            base_word + "!",
            base_word.capitalize(),
            base_word.upper(),
        ]

        for length in range(1, max_length + 1):
            for combo in itertools.product(chars, repeat=length):
                variations.append(base_word + ''.join(combo))

        return variations
