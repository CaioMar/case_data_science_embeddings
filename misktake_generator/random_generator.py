import random
import string

# Expanded common mistakes for Brazilian company names
WORD_MISTAKES = {
    "banco": ["bando", "bancco", "banco "],  # Common typos and extra spaces
    "bradesco": ["bradésco", "bradeskoo"],  
    "itau": ["itaú", "itauu", "itall"],  
    "santander": ["santandér", "santander ", "santanderr"],  
    "caixa": ["cxa", "caíxa", "cacha"],  
    "petrobras": ["petro bras", "petrobrás", "petrobraz"],  
    "vale": ["vale ", "valle", "val"],  
    "eletrobras": ["eletro bras", "elektrobras", "eletrobrás"],  
    "ambev": ["ambév", "ambve", "ambevv"],  
    "jbs": ["jb's", "j b s", "jbz"],  
    "gerdau": ["gerdão", "gerdaú", "ger dau"],  
    "magalu": ["magalú", "magalo", "maga lu"],  
    "ltda": ["limitada", "lt.", "ltdd"],  
    "s.a.": ["sa", "S A", "S/A"],  
    "energia": ["energía", "enérgia", "enerjía"],  
    "telefonica": ["telefônica", "telephonica", "telefónika"],  
    "logistica": ["logística", "logisticaa", "lojyztica"],  
    "indústria": ["industria", "industía", "indústría"],  
}

STOP_WORDS = {"de", "da", "do", "dos", "das", "para", "com", "o", "a", "os", "as", "e", "um", "uma", "uns", "umas"}

def introduce_typos(text: str, num_typos: int = 1) -> str:
    """Generate a string with multiple types of typos for testing."""
    
    if not text or num_typos <= 0:
        return text
    
    typo_functions = [
        swap_chars, delete_char, insert_char, substitute_char, whitespace_error,
        word_substitution, word_omission, word_duplication, stop_word_removal
    ]
    
    words = text.split()
    
    for _ in range(num_typos):
        typo_func = random.choice(typo_functions)
        words = typo_func(words)
    
    return " ".join(words)

# Character-level typos
def swap_chars(words: list) -> list:
    """Swap two adjacent characters in a random word."""
    if not words:
        return words
    idx = random.randint(0, len(words) - 1)
    word = list(words[idx])
    if len(word) > 1:
        swap_idx = random.randint(0, len(word) - 2)
        word[swap_idx], word[swap_idx + 1] = word[swap_idx + 1], word[swap_idx]
        words[idx] = "".join(word)
    return words

def delete_char(words: list) -> list:
    """Randomly delete a character in a word."""
    if not words:
        return words
    idx = random.randint(0, len(words) - 1)
    word = list(words[idx])
    if word:
        del word[random.randint(0, len(word) - 1)]
        words[idx] = "".join(word)
    return words

def insert_char(words: list) -> list:
    """Insert a random character into a word."""
    if not words:
        return words
    idx = random.randint(0, len(words) - 1)
    word = list(words[idx])
    insert_idx = random.randint(0, len(word))
    word.insert(insert_idx, random.choice(string.ascii_letters))
    words[idx] = "".join(word)
    return words

def substitute_char(words: list) -> list:
    """Substitutes a character with a random one."""
    if not words:
        return words
    idx = random.randint(0, len(words) - 1)
    word = list(words[idx])
    if word:
        word[random.randint(0, len(word) - 1)] = random.choice(string.ascii_letters)
        words[idx] = "".join(word)
    return words

def whitespace_error(words: list) -> list:
    """Introduce a whitespace error by adding or removing spaces."""
    if random.random() < 0.5 and len(words) > 1:
        idx = random.randint(0, len(words) - 2)
        words[idx] += words[idx + 1]
        del words[idx + 1]
    else:
        idx = random.randint(0, len(words) - 1)
        words.insert(idx, "")
    return words

# Word-level typos
def word_substitution(words: list) -> list:
    """Replace a word with a similar-sounding mistake."""
    if not words:
        return words
    idx = random.randint(0, len(words) - 1)
    word_lower = words[idx].lower()
    if word_lower in WORD_MISTAKES:
        words[idx] = random.choice(WORD_MISTAKES[word_lower])
    return words

def word_omission(words: list) -> list:
    """Randomly remove a word."""
    if len(words) > 1:
        del words[random.randint(0, len(words) - 1)]
    return words

def word_duplication(words: list) -> list:
    """Duplicate a word randomly."""
    if words:
        idx = random.randint(0, len(words) - 1)
        words.insert(idx, words[idx])
    return words

def stop_word_removal(words: list) -> list:
    """Remove common stop words from the sentence."""
    return [word for word in words if word.lower() not in STOP_WORDS]

# Example usage:
original_text = "Banco do Brasil S.A."
mistyped_text = introduce_typos(original_text, num_typos=3)
print("Original:", original_text)
print("Mistyped:", mistyped_text)
