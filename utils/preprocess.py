import re
import difflib

# Common health keywords that may have typos
KEYWORDS = ["age", "steps", "sleep", "glucose", "heart", "stress", "hydration", "fitness", "diet"]

# Lightweight fuzzy matcher
def correct_keyword(word):
    match = difflib.get_close_matches(word, KEYWORDS, n=1, cutoff=0.7)
    return match[0] if match else word

# Main cleaning + typo-correction function
def clean_input(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove special chars
    words = text.split()
    corrected_words = [correct_keyword(w) for w in words]
    return " ".join(corrected_words)

# For testing/debugging
if __name__ == "__main__":
    sample = "Hi, I m 22 yaer, walk 4000 stpes."
    print(clean_input(sample))
