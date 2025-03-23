import random
import re


def introduce_typos(text: str, temperature: float = 1.0, seed: int = None) -> str:
    """
    Introduces common typos and orthographic errors in a given Portuguese text.

    :param text: The input text.
    :param temperature: Controls randomness (0 = deterministic, 1 = random typos).
    :param seed: Optional random seed for reproducibility.
    :return: Text with introduced typos.
    """
    text = text.lower()

    if seed is not None:
        random.seed(seed)

    typos = [
        (r"qu", "k"),  # "qu" -> "k" (ex: "quebra" -> "kebra")
        (r"ss", "s"),  # "ss" -> "s" (ex: "pressão" -> "presão")
        (r"ç", "c"),  # "ç" -> "c" (ex: "açúcar" -> "acúcar")
        (r"lh", "i"),  # "lh" -> "i" (ex: "trabalho" -> "trabaiho")
        (r"ch", "x"),  # "ch" -> "x" (ex: "chave" -> "xave")
        (r"e[mn]$", ""),  # Dropping final "em/en" (ex: "também" -> "també")
        (r"c(?=[ei])", "s"),  # "c" before "e/i" -> "s" (ex: "cebola" -> "sebóla")
        (r"g(?=[ei])", "j"),  # "g" before "e/i" -> "j" (ex: "gelo" -> "jelo")
        (r"v", "b"),  # "v" -> "b" (ex: "você" -> "bocê")
        (r"m(?=p|b)", "n"),  # "m" before "p/b" -> "n" (ex: "campo" -> "canpo")
    ]

    if temperature == 0:
        random.shuffle(typos, random=lambda: 0)  # Deterministic order
    else:
        random.shuffle(typos)

    for pattern, replacement in typos:
        if random.random() <= temperature:
            text = re.sub(pattern, replacement, text, count=1)

    return text.upper()
