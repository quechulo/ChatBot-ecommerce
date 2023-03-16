import torch

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

    with open('sklep.txt', 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', ' ')
    cmd = 'p'
    while True:

        cmd = input("Enter your question or write 'quit' to quit: ")

        match cmd:
            case 'quit':
                break
            case _:
                query = cmd
                answer = getAnswer(context=data, query=query, only_ans=True)
                print(answer)
