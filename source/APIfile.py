from flask import Flask, request, jsonify
from flask_cors import CORS

from ChatWithGPT import ChatWithGPT
from BERTModel import BERTModel
from loadContexts import load_shoes, load_clothes
from dbReader import insert_conversation_to_db

Session = ChatWithGPT()
Bert = BERTModel()

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

messages = []

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data['message']
    messages.append(message)

    intent = Session.classify_intent(message)
    if Session.intent == 'buty':
        data = load_shoes()
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'ubrania':
        data = load_clothes()
        answer = Bert.get_answer(context=data, query=message, only_ans=True, product_link=True)
    else:
        print('Intent was not buty nor ubrania :( (intent: ' + intent)


    messages.append(answer)


    return jsonify({'query': message,
                    'answer': answer})

@app.route('/receive', methods=['GET'])
def receive_messages():
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)
