from flask import Flask, request, jsonify
from flask_cors import CORS

from ChatWithGPT import ChatWithGPT
from BERTModel import BERTModel
from loadContexts import load_file, load_all_files



app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})


def init_new_context():
    global Session
    Session = ChatWithGPT()
    global Bert
    Bert = BERTModel()
    global messages
    messages = []
    # loading all contexts for BERT
    global shoes
    shoes = load_file('shoes.txt')
    global clothes
    clothes = load_file('clothes.txt')
    global about
    about = load_file('about.txt')
    global orders
    orders = load_file('orders.txt')
    global complaint
    complaint = load_file('complaint.txt')
    global all_context
    all_context = load_all_files('all_context.txt')


@app.route('/send-fresh', methods=['POST'])
def send_fresh_message():
    data_req = request.get_json()
    message = data_req['message']
    sender = data_req['sender']
    messages.append([message, sender])

    intent = Session.classify_intent(message)
    print(intent)
    if Session.intent == 'buty':
        data = shoes
        answer = Bert.get_multiple_answers(context=data, query=message)
    elif Session.intent == 'ubrania':
        data = clothes
        answer = Bert.get_multiple_answers(context=data, query=message)
    elif Session.intent == 'informacje o sklepie':
        data = about
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'zamówienia':
        data = orders
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, product_link=False)
    elif Session.intent == 'reklamacje':
        data = complaint
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, product_link=True)
    elif Session.intent == 'inne':
        answer = 'Niestety nie jestem w stanie odpowiedzieć na to pytanie, proszę zadaj je w inny sposób, albo zapytaj o coś innego.'
    else:
        # handling GPT unavailability case
        data = all_context
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, product_link=True)
        messages.append([answer, 'bot'])
        return jsonify({'query': message,
                        'answer': answer})

    Bert.context = data
    if type(answer) == list:
        answer = Session.full_answer(message, answer[Bert.answer_idx])
        Bert.answer_idx += 1
    else:
        answer = Session.full_answer(message, answer)

    messages.append([answer, 'bot'])
    return jsonify({'query': message,
                    'answer': answer})


@app.route('/send', methods=['POST'])
def send_message():
    data_req = request.get_json()
    message = data_req['message']
    sender = data_req['sender']
    messages.append([message, sender])

    context = Bert.context
    if len(Bert.answers):
        if Bert.answer_idx >= len(Bert.answers):
            answer = "Przepraszam, ale nie mogę znaleźć więcej interesujących Cię produktów\n Naciśnij przycisk 'Zmień temat rozmowy' i spróbuj ponownie"
        else:
            answer = Session.full_answer(message, Bert.answers[Bert.answer_idx])
            Bert.answer_idx += 1
    else:
        answer = Bert.get_simple_answer(context=context, query=message, only_ans=True, page_link=False)

    messages.append([answer, 'bot'])
    return jsonify({'query': message,
                    'answer': answer})


@app.route('/fresh-conversation', methods=['GET'])
def fresh_conversation():
    init_new_context()
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    return jsonify({'status': "Chatbot context was restarted"})

@app.route('/receive', methods=['GET'])
def receive_messages():
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    return jsonify({'messages': messages})


if __name__ == '__main__':
    init_new_context()
    app.run(debug=True)

