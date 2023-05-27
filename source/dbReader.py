from pymongo import MongoClient
from passwords import password, password_write


def insert_conversation_to_db(database, collection_name, document):
    client = get_connection_writer()
    collection = access_db_collection(client, database, collection_name)

    try:
        collection.insert_one(document)
        print("Document inserted successfully!")
        return

    except Exception as e:
        print("Unable to insert documents: ", e)


def get_connection_writer():
    try:
        client = MongoClient(
            f"mongodb+srv://pyWriter:{password_write}@cluster0.bmmwhmg.mongodb.net/?retryWrites=true&w=majority")
        print("Connected successfully!")
        return client

    except Exception as e:
        print("Unable to connect to the cluster: ", e)


def get_connection_reader():
    try:
        client = MongoClient(
            f"mongodb+srv://pyReader:{password}@cluster0.bmmwhmg.mongodb.net/?retryWrites=true&w=majority")
        print("Connected successfully!")
        return client

    except Exception as e:
        print("Unable to connect to the cluster: ", e)


def access_db_collection(client, database, collection_name):
    # Access the database and collection
    try:
        db = client.get_database(database)
        collection = db.get_collection(collection_name)
        print("Database and collection accessed successfully!")
        return collection
    except Exception as e:
        print("Unable to access database or collection: ", e)


def get_all_doc(database, collection_name):
    client = get_connection_reader()
    collection = access_db_collection(client, database, collection_name)

    # Retrieve all documents in the collection
    try:
        documents = collection.find()
        print("Retrieved all documents successfully!")
        return documents

    except Exception as e:
        print("Unable to retrieve documents: ", e)


def write_about_to_file(documents, file_name):
    try:
        # Open the file in write mode
        with open(file_name, "w") as file:
            # Use the truncate() method to erase the contents
            file.truncate()
        # Iterate through each document and print its contents
        for doc in documents:
            content = {
                'contact': doc['contact'],
                'address': doc['address'],
                'email': doc['email'],
                'hello_text': doc['hello_text'],
                'link': 'http://localhost:3000/about',
            }

            add_about_to_file(file_name, content)
    except Exception as e:
        print("Error processing document: ", e)


def add_about_to_file(file_path, content):
    line_to_append = f"{content['hello_text']}.\nMożesz skontaktować się z nami od poniedziłku do piątku w godzinach 9.00-16.00 dzwoniąc pod numer: {content['contact']}, bądź pisząc maila na adres: {content['email']}\nBiuro stacjonarne znajduje się pod adresem: {content['address']}\n(*link*{content['link']}*link*)\n"
    with open(file_path, "a", encoding='utf-8') as file:
        file.write(line_to_append)


def write_complaint_to_file(documents, file_name):
    try:
        # Open the file in write mode
        with open(file_name, "w") as file:
            # Use the truncate() method to erase the contents
            file.truncate()
        # Iterate through each document and print its contents
        for doc in documents:
            content = {
                'content': doc['content'],
                'link': 'http://localhost:3000/zwroty',
            }

            add_complaint_to_file(file_name, content)
    except Exception as e:
        print("Error processing document: ", e)


def add_complaint_to_file(file_path, content):
    line_to_append = f"{content['content']}(*link*{content['link']}*link*)\n"
    with open(file_path, "a", encoding='utf-8') as file:
        file.write(line_to_append)


def write_to_file(documents, file_name):
    try:
        # Open the file in write mode
        with open(file_name, "w") as file:
            # Use the truncate() method to erase the contents
            file.truncate()
        # Iterate through each document and print its contents
        for doc in documents:
            product = {
                'type_of_product': doc['type'],
                'brand': doc['brand'],
                'description': doc['description'],
                'name': doc['name'],
                'photos': doc['photos'],
                'color': doc['color'],
                'gender': doc['gender'],
                'price': doc['price'],
                'link': doc['_id'],
            }
            add_dict_to_file(file_name, product)

    except Exception as e:
        print("Error processing document: ", e)


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
        line_to_append = f"{category[product['type_of_product']]} {gender_e[product['gender']]} {product['color']} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*http://localhost:3000/produkty/buty/{product['link']}*link*).\n"
    elif product['type_of_product'] == 'tracksuit':
        line_to_append = f"{category[product['type_of_product']]} {gender_i[product['gender']]} {product['color']} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*http://localhost:3000/produkty/ubrania/{product['link']}*link*).\n"
    else:
        line_to_append = f"{category[product['type_of_product']]} {gender_a[product['gender']]} {product['color']} {product['brand']} {product['name']} cena {product['price']}PLN ,  (*link*http://localhost:3000/produkty/ubrania/{product['link']}*link*).\n"
    print(line_to_append)
    with open(file_path, "a", encoding='utf-8') as file:
        file.write(line_to_append)


# Set up the connection to the MongoDB Atlas database
if __name__ == '__main__':
    shoes = get_all_doc('products', 'shoes')
    write_to_file(shoes, 'shoes.txt')

    clothes = get_all_doc('products', 'clothes')
    write_to_file(clothes, 'clothes.txt')

    about = get_all_doc('info', 'about')
    write_about_to_file(about, 'about.txt')

    complaint = get_all_doc('info', 'complaints')
    write_complaint_to_file(complaint, 'complaint.txt')

    # test insertion to db:
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': ['hello chatbot!', 'Hello human friend!']})
