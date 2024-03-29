from flask import Flask, request, jsonify
from flask_cors import CORS

from ChatWithGPT import ChatWithGPT
from BERTModel import BERTModel
from loadContexts import load_file, load_all_files
from dbReader import insert_conversation_to_db

Session = ChatWithGPT()
Bert = BERTModel()

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

messages = []
# loading all contexts for BERT
shoes = load_file('shoes.txt')
clothes = load_file('clothes.txt')
about = load_file('about.txt')
orders = load_file('orders.txt')
complaint = load_file('complaint.txt')
all_context = load_all_files('all_context.txt')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    sender = data['sender']
    messages.append([message, sender])

    intent = Session.classify_intent(message)
    print(intent)
    if Session.intent == 'buty':
        data = shoes
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'ubrania':
        data = clothes
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'informacje o sklepie':
        data = about
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'zamówienia':
        data = orders
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=False)
    elif Session.intent == 'reklamacje':
        data = complaint
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'inne':
        answer = 'Niestety nie jestem w stanie odpowiedzieć na to pytanie, proszę zadaj je w inny sposób, albo zapytaj o coś innego.'
    else:
        # handling GPT unavailability case
        data = all_context
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
        messages.append([answer, 'bot'])
        return jsonify({'query': message,
                        'answer': answer})

    answer = Session.full_answer(message, answer)

    messages.append([answer, 'bot'])
    return jsonify({'query': message,
                    'answer': answer})

@app.route('/receive', methods=['GET'])
def receive_messages():
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
