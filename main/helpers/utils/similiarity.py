import re
from Levenshtein import distance as levenshtein_distance
from nltk.util import ngrams
from metaphone import doublemetaphone
from unidecode import unidecode

class AdvancedSimilarityChecker:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def preprocess(self, text):
        return unidecode(text.lower())

    def levenshtein_similarity(self, s1, s2):
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1 - levenshtein_distance(s1, s2) / max_len

    def ngram_similarity(self, s1, s2, n=2):
        s1_ngrams = set(ngrams(s1, n))
        s2_ngrams = set(ngrams(s2, n))
        intersection = len(s1_ngrams.intersection(s2_ngrams))
        union = len(s1_ngrams.union(s2_ngrams))
        return intersection / union if union > 0 else 0

    def phonetic_similarity(self, s1, s2):
        code1 = doublemetaphone(s1)
        code2 = doublemetaphone(s2)
        return 1 if code1 == code2 else 0

    def calculate_similarity(self, text1, text2):
        text1 = self.preprocess(text1)
        text2 = self.preprocess(text2)

        lev_sim = self.levenshtein_similarity(text1, text2)
        ngram_sim = self.ngram_similarity(text1, text2)
        phonetic_sim = self.phonetic_similarity(text1, text2)

        # Weighted average of similarities
        total_sim = (0.5 * lev_sim) + (0.3 * ngram_sim) + (0.2 * phonetic_sim)
        return total_sim

    def is_similar(self, text1, text2):
        return self.calculate_similarity(text1, text2) >= self.threshold