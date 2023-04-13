import openai

# load and set our key
openai.api_key = open("../key.txt", "r").read().strip("\n")


class ChatWithGPT:
    def __init__(self):
        self.message_log = []
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

    def full_answer(self, question, answer):
        quest = f"odpowiedz na pytanie '{question}' pełnym zdaniem, gdzie odpowiedzią jest '{answer}'."
        full_ans = self.ask_chat_gpt(quest)

        return full_ans

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
            return "Unfortunately Chatgpt is unavailable right now :("

        assistant_reply = completion.choices[0].message.content
        self.message_log.append({"role": "assistant", "content": f"{assistant_reply}"})

        if not write_log:
            self.message_log.pop()
            self.message_log.pop()

        return assistant_reply
