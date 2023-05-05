from pymongo import MongoClient
from passwords import password

database = 'products'
collection = 'clothes'

def add_dict_to_file(file_path, product):
    category = {
        'sneakers': 'buty',
        'flipflops': 'klapki',
        'jacket': 'kurtka',
        'tracksuit': 'dres',
        'tshirt': 'koszulka',
    }
    gender_e = {
        'male': 'męskie',
        'female': 'damskie',
        'unisex': 'unisex'
    }
    gender_a = {
        'male': 'męska',
        'female': 'damska',
        'unisex': 'unisex'
    }
    gender_i = {
        'male': 'męski',
        'female': 'damski',
        'unisex': 'unisex'
    }

    if product['type_of_product'] == 'sneakers' or product['type_of_product'] == 'flipflops':
        line_to_append = f"{category[product['type_of_product']]} {gender_e[product['gender']]} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*{product['link']}*link*).\n"
    elif product['type_of_product'] == 'tracksuit':
        line_to_append = f"{category[product['type_of_product']]} {gender_i[product['gender']]} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*{product['link']}*link*).\n"
    else:
        line_to_append = f"{category[product['type_of_product']]} {gender_a[product['gender']]} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*{product['link']}*link*).\n"
    print(line_to_append)
    with open(file_path, "a", encoding='utf-8') as file:
        file.write(line_to_append)


# Set up the connection to the MongoDB Atlas database
try:
    client = MongoClient(f"mongodb+srv://pyReader:{password}@cluster0.bmmwhmg.mongodb.net/?retryWrites=true&w=majority")
    print("Connected successfully!")
except Exception as e:
    print("Unable to connect to the cluster: ", e)

# Access the database and collection
try:
    db = client.get_database(database)
    collection = db.get_collection(collection)
    print("Database and collection accessed successfully!")
except Exception as e:
    print("Unable to access database or collection: ", e)

# Retrieve all documents in the collection
try:
    documents = collection.find()
    print("Retrieved all documents successfully!")
except Exception as e:
    print("Unable to retrieve documents: ", e)

# Iterate through each document and print its contents
try:
    for doc in documents:
        product = {
            'type_of_product': doc['type'],
            'brand': doc['brand'],
            'description': doc['description'],
            'name': doc['name'],
            'photos': doc['photos'],
            'color': [doc['color']],
            'gender': doc['gender'],
            'price': doc['price'],
            'link': doc['_id'],  # TODO add link to product
        }

        add_dict_to_file('clothes.txt', product)


except Exception as e:
    print("Error processing documents: ", e)
