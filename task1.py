class Question():

    def __init__(self, text, options):

        self.options = options

        self.votes = {}

        for i in self.options:

            self.votes[i] = 0

        self.text = text

        self.quantity = 0

        self.winner_ = ''

    def vote(self, option_index):

        if 0<=option_index<len(self.options):

            self.votes[self.options[option_index]] += 1

            self.quantity += 1

            return True
        
        else:

            return False
        
    def get_results(self):

        return self.votes
    
    def total_votes(self):

        return self.quantity
    
    def winner(self):
        max_votes = max(self.votes.values())
        
        leaders = [opt for opt, cnt in self.votes.items() if cnt == max_votes]
        
        if len(leaders) > 1:
        
            return None
        
        self.winner_ = leaders[0] 
        
        return leaders[0]    
        
class Participant():

    def __init__(self, name, email):

        self.name = name

        self.email = email

        self.voted_questions = []

    def has_voted_in(self, question_id):

        return question_id in self.voted_questions
    
    def add_voted_question(self, question_id):

        self.voted_questions.append(question_id)

class Poll():

    def __init__(self):

        self.questions = []

        self.participants = []

        self.next_question_id = 0

    def add_question(self, question):

        self.questions.append(question)

        question.id = self.next_question_id

        self.next_question_id += 1

    def add_participant(self, participant):

        self.participants.append(participant)
    
    def find_participant_by_email(self, email):

        for i in self.participants:

            if email == i.email:

                return i
        return None

    def find_question_by_index(self, index):

        if 0 <= index < len(self.questions):

            return self.questions[index]
        
        return None
    
    def cast_vote(self, participant_email, question_index, option_index):

        participant = self.find_participant_by_email(participant_email)

        question = self.find_question_by_index(question_index)

        if not participant:

            return "Участник не найден"
        
        elif not question:
            
            return "Вопрос не найден"
        
        elif participant.has_voted_in(question.id):

            return "Участник уже голосовал в этом вопросе"
        
        elif not question.vote(option_index):

            return "Неверный вариант ответа"
        
        participant.add_voted_question(question.id)

        return "Голос принят"

        

        

    def get_question_statistics(self, question_index):

        question = self.find_question_by_index(question_index)
        
        if not question:
        
            return "Вопрос не найден"

        lines = [f"Вопрос: {question.text}"]

        for option, count in question.get_results().items():

            lines.append(f"{option}: {count} голосов")   # можно "голоса/голосов"

        lines.append(f"Всего голосов: {question.total_votes()}")

        winner = question.winner()

        if winner is None:

            if question.total_votes() == 0:

                lines.append("Победитель: нет")

            else:

                lines.append("Победитель: ничья")

        else:

            lines.append(f"Победитель: {winner}")


        return "\n".join(lines)
    


# Тест 1: создание вопроса и подсчёт голосов
q = Question("Тест?", ["A", "B"])
q.vote(0)
q.vote(0)
q.vote(1)
assert q.total_votes() == 3
assert q.winner() == "A"
assert q.get_results() == {"A": 2, "B": 1}
print("Тест 1 пройден")

# Тест 2: некорректное голосование
q2 = Question("Опрос", ["Да", "Нет"])
assert q2.vote(2) == False   # неверный индекс
assert q2.total_votes() == 0
print("Тест 2 пройден")

# Тест 3: участник не может голосовать дважды
poll = Poll()
q3 = Question("Вопрос", ["1", "2"])
poll.add_question(q3)
user = Participant("Иван", "ivan@ya.ru")
poll.add_participant(user)
res1 = poll.cast_vote("ivan@ya.ru", 0, 0)
res2 = poll.cast_vote("ivan@ya.ru", 0, 1)
assert res1 == "Голос принят"
assert "уже голосовал" in res2.lower()
print("Тест 3 пройден")

# Тест 4: поиск победителя при ничьей
q4 = Question("Ничья", ["X", "Y"])
q4.vote(0)
q4.vote(1)
assert q4.winner() is None
print("Тест 4 пройден")