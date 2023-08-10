import torch


from loadContexts import load_file, load_all_files
from dbReader import insert_conversation_to_db



class BERTModel:
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        print("Device:", self.device)
        self.qa_pipeline = torch.load('bert-base-multi')
        self.answers = None
        self.answers_idx = 0
        self.end_of_ans = 0
        self.intent = None
        self.context = None

    def get_answer(self, context, query, only_ans=True, product_link=False):
        result = self.qa_pipeline({
            'context': context,
            'question': query
        })
        start_idx = int(result['end'])
        self.end_of_ans = start_idx

        cut_start = int(result['start'])
        cut_end = int(result['end'])
        char = context[cut_start]
        while (char != "\n") and cut_start > 0:
            cut_start -= 1
            char = context[cut_start]
        char = context[cut_end]
        while (char != "*") and (cut_start < len(context) - 1):
            cut_end += 1
            char = context[cut_end]

        if context[cut_start] == "\n":
            cut_start += 1

        result['answer'] = context[cut_start:cut_end - 5]

        link_to_product = ''
        if product_link:
            link_to_product = context[start_idx:].split('*link*')[1]
            result['link'] = link_to_product

            # result['answer'] = result['answer'] + ' link do produktu: ' + link_to_product
        if only_ans and product_link:
            return {'answer': result['answer'], 'link': result['link']}

        if only_ans:
            return result['answer']
        else:
            return result

    def get_multiple_answers(self, context, query):
        score = 1
        # Clear previous messages
        self.answers = []

        while score > 0.0001:
            answer = self.get_answer(context, query, only_ans=False, product_link=True)
            self.answers.append({'answer': answer['answer'], 'link': answer['link']})

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
            print(f"Answer: {score}---------- ", answer)

        if len(self.answers) > 1:
            self.answers.pop()
            print("Bert.answers: ", self.answers)

        return self.answers

    def get_simple_answer(self, context, query, only_ans=False, page_link=True):
        result = self.qa_pipeline({
            'context': context,
            'question': query
        })
        start_idx = int(result['end'])

        result['link'] = ""
        if page_link:
            link_to_page = context[start_idx:].split('*link*')[1]
            result['link'] = link_to_page
            # result['answer'] = result['answer'] + ' link do strony: ' + link_to_page

        if only_ans:
            return {'answer': result['answer'], 'link': result['link']}
        else:
            return result

    def get_order_details(self, context, query, user, only_ans=True):
        result = self.qa_pipeline({
            'context': context,
            'question': query
        })
        start_idx = int(result['end'])

        # Logic to verify whether answer is users order

        if only_ans:
            return result['answer']
        else:
            return result

if __name__ == '__main__':
    Bert = BERTModel()
    message = 'Szukam butów damskich'
    data = load_file('shoes.txt')

    x = Bert.get_simple_answer(context=data, query=message)
    print(x)
    print("Answers: \n", Bert.answers)
