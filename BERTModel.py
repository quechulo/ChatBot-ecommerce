import torch
class BERTModel:
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        print("Device:", self.device)
        self.qa_pipeline = torch.load('bert-base-multi')
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

        if only_ans:
            answer = result['answer']
            if product_link:
                return answer + ' link do produktu: ' + link_to_product
            return result['answer']
        else:
            return result
