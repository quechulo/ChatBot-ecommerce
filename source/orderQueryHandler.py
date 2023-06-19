from pymongo import MongoClient
from passwords import password
from source.dbReader import get_connection_reader, access_db_collection
from bson.objectid import ObjectId
import re


def get_document(order_id, database='orders', collection_name='all_orders'):
    client = get_connection_reader()
    collection = access_db_collection(client, database, collection_name)
    document = collection.find_one({"_id": ObjectId(order_id)})

    return document


def is_valid_objectId(string):
    try:
        ObjectId(string)
        return True
    except:
        return False


def order_query(email, message):
    order_id = handle_message(message)
    valid_id = is_valid_objectId(order_id)

    if valid_id:
        doc = get_document(order_id)
        if doc['email'] == email:
            return doc['status']
        else:
            return 'Niestety nie mogę udzielić informacji o tym zamówieniu. Skorzystaj z innego konta.'
    else:
        return 'Pamiętaj aby pytanie dotyczące zamówienia miało formę: "Jaki jest status zamówienia <id_zamówienia>".'


def handle_message(msg):
    id_number = msg.split()[-1]
    if len(id_number) < 13:
        id_number = msg.split()[-2]
    # get rid of any accidental special chars
    id_number = re.sub('[^A-Za-z0-9]+', '', id_number)

    return id_number


if __name__ == '__main__':
    # print(order_query('fecosen627@anwarb.com', 'jaki jest numer zamówienia 648af522da7c8efb6c295f0b?'))
    print(order_query('fecosen627@anwarb.com', 'jaki jest numer zamówienia 648af522da7c8efb6c295f0b?'))
