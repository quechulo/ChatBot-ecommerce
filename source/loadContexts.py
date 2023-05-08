def load_shoes():
    with open('shoes.txt', 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', ' ')
    return data

def load_clothes():
    with open('clothes.txt', 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', ' ')
    return data