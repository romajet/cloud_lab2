import re

class WordSorter:
    def __init__(self, text: str):
        self.text = text

    def get_sorted_unique_words(self):
        # Разделение на слова с учетом символов и регистра
        words = re.findall(r'\b\w+\b', self.text.lower())
        unique_sorted_words = sorted(set(words))
        return unique_sorted_words

    def get_formatted_output(self):
        return "\n".join(self.get_sorted_unique_words())
