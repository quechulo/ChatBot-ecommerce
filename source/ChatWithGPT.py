import openai

# load and set our key
openai.api_key = open("../key.txt", "r").read().strip("\n")


class ChatWithGPT:
    def __init__(self):
        self.message_log = []
        self.message_log.append({"role": "system", "content": f"Jesteś wirtualnym asystentem na stronie ecommerce BuyStuff. Zapewniasz użytkownikom strony jak najlepszą obsługę kienta."})
        # tutaj dodac wiadomosc aby chatgpt wczul sie w role wirtualnego asystenta na stronie ecommerce
        self.intent = None

    def format_query(self, question):
        # return question.replace('"', '')  # TODO think how to format query / if format ever
        return question

    def classify_intent(self, question):
        quest = f"Zakwalifikuj pytanie '{question}' do jednej z podanych kategorii: 'buty', 'ubrania', 'zamówienia', 'informacje o sklepie', 'reklamacje', 'inne'. W odpowiedzi podaj tylko wybraną kategorię."
        intention = self.ask_chat_gpt(quest, write_log=False)
        intention = intention.lower()
        if "buty" in intention:
            intention = 'buty'
        elif "ubrania" in intention:
            intention = 'ubrania'
        elif "zamówienia" in intention:
            intention = 'zamówienia'
        elif "informacje o sklepie" in intention:
            intention = 'informacje o sklepie'
        elif "reklamacje" in intention:
            intention = 'reklamacje'
        elif "inne" in intention:
            intention = 'inne'

        self.intent = intention
        return intention

    def is_question_about_shop(self, question):
        quest = f"Aktualny temat rozmowy to: {self.intent}. Odpowiedz tak lub nie, czy pytanie '{question}' obejmuje kompetencje chatbota na stronie ecommerce rozmawiając na podany wcześniej temat? W odpowiedzi napisz jedynie tak lub nie."
        answer = self.ask_chat_gpt(quest, write_log=False)
        answer = answer.lower()
        print("is_question_about_shop: ", answer)
        if "nie" in answer:
            answer = False
        elif "tak" in answer:
            answer = True
        else:
            answer = False

        print("is_question_about_shop ",answer)
        return answer

    def full_answer(self, question, answer):
        quest = f"odpowiedz na pytanie '{question}' pełnym zdaniem, gdzie odpowiedzią jest '{answer}'."
        full_ans = self.ask_chat_gpt(quest, write_log=True)
        if "unavailable" in full_ans:
            print("GPT was not able to create full answer")
            return answer

        return full_ans

    def get_most_suitable_ans(self, question, answers):
        quest = f"Odpowiedz na pytanie '{question}' pełnym zdaniem, wybierając spośród odpowiedzi: '{answers}' jedną najbardziej dopasowaną do pytania."
        ans = self.ask_chat_gpt(quest, write_log=True)
        if "unavailable" in ans:
            print("GPT was not able to get most suitable answer")
            return answers[0]
        return ans

    def ask_chat_gpt(self, question, write_log=True):
        try:
            question = self.format_query(question)
        except:
            return "Please enter valid question"
        self.message_log.append({"role": "user", "content": f"{question}"})
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
                messages=self.message_log
            )
        except:
            return "unfortunately chatgpt is unavailable right now :("

        assistant_reply = completion.choices[0].message.content
        self.message_log.append({"role": "assistant", "content": f"{assistant_reply}"})

        if not write_log:
            self.message_log.pop()
            self.message_log.pop()

        return assistant_reply
