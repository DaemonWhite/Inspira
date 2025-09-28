def add_without_duplicate(liste: list, word: str):
    if word.lower() not in (m.lower() for m in liste):
        liste.append(word)
