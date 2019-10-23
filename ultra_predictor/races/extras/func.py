def itra_name_extractor(name):
    """Extract name where last name is uppercase"""
    last_name = []
    first_name = []
    words = name.split(" ")
    for word in words:
        if word.isupper():
            last_name.append(word)
        else:
            first_name.append(word)

    return {"first_name": " ".join(first_name), "last_name": " ".join(last_name)}

