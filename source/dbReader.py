from pymongo import MongoClient
from passwords import password
import json

database = 'products'

def add_dict_to_file(file_path, dict_content):
    category = {
        'sneakers': 'buty',
        'flipflops': 'klapki',
    }
    gender = {
        'male': 'męskie',
        'female': 'damskie',
        'unisex': 'damskie i męskie, unisex'
    }
    line_to_append = f"{gender[product['gender']]} {category[product['type_of_product']]} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*f{product['link']}).\n"
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
    db = client.get_database(f"{database}")
    collection = db.get_collection("shoes")
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
            'link': 'link-to-product',  # TODO add link to product
        }

        add_dict_to_file('shoes.txt', product)


except Exception as e:
    print("Error processing documents: ", e)
