from ChatWithGPT import ChatWithGPT
from source.BERTModel import BERTModel
from loadContexts import load_shoes

import time


if __name__ == '__main__':
    Session = ChatWithGPT()
    Bert = BERTModel()

    # query = "Czy posiadacie w swojej ofercie męskie buty Nike?"
    query = "Czy posiadacie w swojej ofercie buty Nike?"

    start_total_time = time.time()  # TIME measure
    start_time = time.time()  # TIME measure

    # intent = Session.classify_intent(query)
    # print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure

    # if session.intent == 'buty':
    #     data = load_shoes()
    data = load_shoes()

    # print('Klasyfikacja pytania: ', intent)

    start_time = time.time()  # TIME measure

    answer = Bert.get_answer(context=data, query=query, only_ans=True, product_link=True)

    print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure
    print('Answer from BERT: ', answer)

    start_time = time.time()  # TIME measure

    ans = Session.full_answer(query, answer)
    print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure
    print('Odpowiedź Chatbota: ', ans)

    print('Total time: ', round(time.time() - start_total_time, 2), 's')  # TIME measure

