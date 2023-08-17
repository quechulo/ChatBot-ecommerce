from flask import Blueprint, request, jsonify
from app.ChatWithGPT import ChatWithGPT
from app.BERTModel import BERTModel
from app.loadContexts import load_file, load_all_files

from source.orderQueryHandler import order_query

bp = Blueprint('main', __name__)


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


init_new_context()


@bp.route('/')
def home():
    return "Welcome to the BuyStuff Chatbot's API"


@bp.route('/send-fresh', methods=['POST'])
def send_fresh_message():
    data_req = request.get_json()
    message = data_req['message']
    sender = data_req['sender']
    user_email = data_req['userEmail']
    print('user email: ', user_email)  # TODO line just for testing!
    messages.append([message, sender, ""])

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
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, page_link=True)
    elif Session.intent == 'zamówienia':
        answer = order_query(user_email, message)
        answer = Session.full_answer(message, answer)
        messages.append([answer, 'bot', ""])
        # Special sender in return statement handling
        return jsonify({'query': message,
                        'answer': answer,
                        'sender': 'order_query'})
    elif Session.intent == 'reklamacje':
        data = complaint
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, page_link=True)
    elif Session.intent == 'inne':
        answer = 'Niestety nie jestem w stanie odpowiedzieć na to pytanie, proszę zadaj je w inny sposób, albo zapytaj o coś innego.'
        messages.append([answer, 'bot', ""])
        return jsonify({'query': message,
                        'answer': answer,
                        'sender': 'bot'})
    else:
        # handling GPT unavailability case
        data = all_context
        answer = Bert.get_simple_answer(context=data, query=message, only_ans=True, page_link=True)
        messages.append([answer['answer'], 'bert', answer['link']])
        return jsonify({'query': message,
                        'answer': answer['answer'],
                        'link': answer['link'],
                        'sender': 'bert'})

    Bert.context = data
    if type(answer) == list:
        ans = Session.full_answer(message, answer[0]['answer'])
        link = answer[Bert.answers_idx]['link']
        answer = {'answer': ans, 'link': link}
        Bert.answers.pop(0)
    else:
        ans = Session.full_answer(message, answer['answer'])
        link = answer['link']
        answer = {'answer': ans, 'link': link}

    messages.append([answer['answer'], 'bot', answer['link']])
    return jsonify({'query': message,
                    'answer': answer['answer'],
                    'link': answer['link'],
                    'sender': 'bot'})


@bp.route('/send', methods=['POST'])
def send_message():
    data_req = request.get_json()
    message = data_req['message']
    sender = data_req['sender']
    messages.append([message, sender, ""])

    context = Bert.context
    if type(Bert.answers) == list and len(Bert.answers) > 0:
        if Session.is_question_about_shop(message):
            answer = Session.get_most_suitable_ans(message, Bert.answers)
            print(f"selected index {answer['idx_to_rm']} from array {Bert.answers}")
            try:
                Bert.answers.pop(answer['idx_to_rm'])
            except:
                print(f"unable to pop index {answer['idx_to_rm']} from array {Bert.answers}")
            ans = answer['answer']
            link = answer['link']
        else:
            ans = "Przepraszam, ale nie jestem w stanie odpowiedzieć na to pytanie.\n Wychodzi ono poza moje kompetencje. Naciśnij przycisk 'Zmień temat rozmowy' i spróbuj ponownie zapytać o inne nasze produkty."
            link = ""
            # answer = Session.full_answer(message, Bert.answers[Bert.answer_idx])
            # Bert.answer_idx += 1
    elif type(Bert.answers) == list and len(Bert.answers) == 0:
        ans = "Przepraszam, ale nie mogę znaleźć więcej interesujących Cię produktów.\n Naciśnij przycisk 'Zmień temat rozmowy' i spróbuj ponownie"
        link = ""
    else:
        answer = Bert.get_simple_answer(context=context, query=message, only_ans=True, page_link=True)
        print("Bert simple answer inside /send", answer)
        ans = Session.full_answer(message, answer['answer'])
        link = answer['link']


    messages.append([ans, 'bot',  link])
    return jsonify({'query': message,
                    'answer': ans,
                    'link': link})


@bp.route('/fresh-conversation', methods=['GET'])
def fresh_conversation():
    #  store conversation to DB
    # if len(messages) > 0:
    #     insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    init_new_context()

    return jsonify({'status': "Chatbot context was restarted"})

@bp.route('/receive', methods=['GET'])
def receive_messages():
    # insert_conversation_to_db('chatbot', 'conversations', {'messages': messages})
    return jsonify({'messages': messages})

