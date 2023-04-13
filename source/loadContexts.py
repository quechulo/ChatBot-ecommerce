def load_shoes():
    with open('shoes.txt', 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', ' ')
    return data