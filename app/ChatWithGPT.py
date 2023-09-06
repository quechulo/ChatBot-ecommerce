import os

from fuzzywuzzy import fuzz
import openai
import os
from dotenv import load_dotenv

# load and set our key
load_dotenv()
openai.api_key = os.environ.get('OPEN_AI_KEY')


class ChatWithGPT:
    def __init__(self):
        self.message_log = []
        self.message_log.append({"role": "system", "content": f"Jesteś wirtualnym asystentem na stronie ecommerce BuyStuff. Zapewniasz użytkownikom strony jak najlepszą obsługę kienta. Odpowiadasz na zadane pytania na temat, korzystasz jedynie z wiedzy która jest zawarta w kontekście."})
        self.intent = None

    def format_query(self, question):
        # return question.replace('"', '')  # TODO think how to format query / if format ever
        return question

    def classify_intent(self, question):
        quest = f"Zakwalifikuj pytanie '{question}' do jednej z podanych kategorii: 'buty', 'ubrania', 'status zamówienia', 'informacje o sklepie', 'reklamacje', 'inne'. W odpowiedzi podaj tylko wybraną kategorię. Przykład: pytanie:'Szukam męskich butów sportowych', odpowiedź:'buty'"
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
        quest = f"Aktualny temat rozmowy to: {self.intent}. Odpowiedz tak lub nie, czy pytanie, bądź stwierdzenie: '{question}' mogłoby paść podczas konwersacji z chatbotem na stronie ecommerce. W odpowiedzi napisz jedynie tak lub nie."
        answer = self.ask_chat_gpt(quest, write_log=False)
        answer = answer.lower()
        print("is_question_about_shop: ", answer)
        if "nie" in answer:
            answer = False
        elif "tak" in answer:
            answer = True
        else:
            answer = False

        print("is_question_about_shop ", answer)
        return answer

    def full_answer(self, question, answer):
        quest = f"napisz odpowiedź na pytanie '{question}' pełnym zdaniem, gdzie odpowiedzią jest '{answer}'. W odpowiedzi nie zawieraj odpowiedzi twierdzącej o tym, że ją napiszesz. Staraj się, aby odpowiedzi nie były za każdym razem tak samo skonstruowane. Miej na uwadze, że po odpowiedzi, którą wygenerujesz będzie wstawiony link do produktu lub strony, jednak nie wprowadzaj tam tekstu który ma udawać link bądź nie wstawiaj miejsca do jego wstawienia. Przykład zły: 'Sprawdź je tutaj: link do produktu', przykład dobry: 'Zapoznaj się z nim tutaj:', przykład dobry: 'Więcej informacji znajdziesz tu:'. Takim zwrotem wiadomość ma się kończyć. Kiedy pytanie dotyczy statusu zamówienia, nie będzie żadnego linku, więc zakończ zdanie mając to na uwadze."
        full_ans = self.ask_chat_gpt(quest, write_log=True)
        if "unavailable" in full_ans:
            print("GPT was not able to create full answer")
            return answer

        return full_ans

    def get_most_suitable_ans(self, question, answers):
        values = []
        for entry in answers:
            values.append(entry['answer'])
        quest = f"Odpowiedz na pytanie '{question}' pełnym zdaniem, wybierając spośród odpowiedzi: '{values}' jedną najbardziej dopasowaną do pytania."
        ans = self.ask_chat_gpt(quest, write_log=True)
        link = ""

        if "unavailable" in ans:
            print("GPT was not able to get most suitable answer")
            answers[0]['link'] = link
            answers[0]['idx_to_rm'] = 0
            return answers[0]


        #  Getting link to chosen answer by calculating differences between sequences
        similarity_dist = [(string, fuzz.partial_ratio(ans, string)) for string in values]
        most_similar = max(similarity_dist, key=lambda x: x[1])
        idx_of_link = values.index(most_similar[0])

        try:
            link = answers[idx_of_link]['link']
        except:
            print("get_most_suitable_ans FAILED")


        return {'answer': ans, 'link': link, 'idx_to_rm': idx_of_link}

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
            return "unfortunately GPT is unavailable right now :("

        assistant_reply = completion.choices[0].message.content
        self.message_log.append({"role": "assistant", "content": f"{assistant_reply}"})

        if not write_log:
            self.message_log.pop()
            self.message_log.pop()

        return assistant_reply
