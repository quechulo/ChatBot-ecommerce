import torch


from loadContexts import load_file, load_all_files
from dbReader import insert_conversation_to_db



class BERTModel:
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        print("Device:", self.device)
        self.qa_pipeline = torch.load('bert-base-multi')
        self.answers = []
        self.end_of_ans = 0
        self.intent = None

    def get_answer(self, context, query, only_ans=True, product_link=False):
        result = self.qa_pipeline({
            'context': context,
            'question': query
        })
        start_idx = int(result['end'])
        self.end_of_ans = start_idx
        if product_link:
            link_to_product = context[start_idx:].split('*link*')[1]
            result['answer'] = result['answer'] + ' link do produktu: ' + link_to_product

        if only_ans:
            return result['answer']
        else:
            return result

    def get_multiple_answers(self, context, query):
        score = 1
        # Clear previous messages
        self.answers = []

        i = 0
        while score > 0.0001:
            answer = self.get_answer(context, query, only_ans=False, product_link=True)
            answers.append(answer['answer'])

            start_idx = int(answer['start'])
            end_idx = int(answer['end'])
            score = float(answer['score'])


            cut_start = start_idx
            cut_end = end_idx
            char = context[cut_start]
            while (char != "\n") and cut_start > 0:
                cut_start -= 1
                char = context[cut_start]
            char = context[cut_end]
            while (char != "\n") and (cut_start < len(context)-1):
                cut_end += 1
                char = context[cut_end]

            context = context[:cut_start] + context[cut_end:]
            print(context)
            print(f"Answer: -{score}---------- ", answer)
            i += 1
        if len(answers) > 1:
            self.answers = answers[:-1]
            return answers[:-1]
        else:
            self.answers = answers
            return answers


if __name__ == '__main__':
    Bert = BERTModel()
    message = 'Szukam butów damskich'
    data = load_file('shoes.txt')

    answers = Bert.get_multiple_answers(context=data, query=message)
    print("Answers: \n", answers)
