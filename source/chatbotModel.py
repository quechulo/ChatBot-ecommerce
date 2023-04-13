import torch
from ChatWithGPT import ChatWithGPT
from loadContexts import load_shoes

import time

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
print("Device:", device)
qa_pipeline = torch.load('bert-base-multi')


def getAnswer(context, query, only_ans=True):
    result = qa_pipeline({
        'context': context,
        'question': query
    })
    if only_ans:
        return result['answer']
    else:
        return result

if __name__ == '__main__':
    session = ChatWithGPT()

    # query = "Czy posiadacie w swojej ofercie męskie buty Nike?"
    query = "Jaka jest cena męskich butów Nike?"

    start_total_time = time.time()  # TIME measure
    start_time = time.time()  # TIME measure

    intent = session.classify_intent(query)
    print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure

    if session.intent.lower() == 'buty':
        data = load_shoes()

    print('Klasyfikacja pytania: ', intent)

    start_time = time.time()  # TIME measure

    answer = getAnswer(context=data, query=query, only_ans=True)

    print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure
    print('Answer from BERT: ', answer)

    queryGpt = f"odpowiedz na pytanie '{query}' pełnym zdaniem, gdzie odpowiedzią jest '{answer}'."

    start_time = time.time()  # TIME measure

    ans = session.ask_chat_gpt(queryGpt)
    print('-----------time: ', round(time.time() - start_time, 2), 's')  # TIME measure
    print('Odpowiedź Chatbota: ', ans)

    print('Total time: ', round(time.time() - start_total_time, 2), 's')  # TIME measure
