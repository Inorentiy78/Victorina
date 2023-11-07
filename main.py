import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QMessageBox, QTextBrowser

class QuestionParser:
    def __init__(self, questions_file, answers_file):
        self.questions_file = questions_file
        self.answers_file = answers_file

    def read_questions_and_answers(self):
        questions = []
        with open(self.questions_file, "r", encoding="utf-8") as questions_file:
            question_data = questions_file.read().split("---\n")

        with open(self.answers_file, "r", encoding="utf-8") as answers_file:
            answer_data = answers_file.read().split("\n")

        if len(questions) == len(answers):
            all_index = random.sample(range(len(questions)), 5)  # Randomly sample 5 unique indices

            my_questions = []  # Create an empty list to store your selected questions
            for i in all_index:
                my_questions.append({
                    "vopros": questions[i]["question"],
                    "answers": questions[i]["options"],
                    "correct_answers": answers[i]
                })

        for question_block, answer_line in zip(question_data, answer_data):
            question_lines = question_block.split("\n")
            question = {
                "question": question_lines[0],
                "options": question_lines[1:5],
                "correct_answer": int(answer_line.split(": ")[1]) 
            }
            questions.append(question)

        

        # Shuffle the questions and select the first 25
        random.shuffle(questions)
        selected_questions = questions[:5]
        print(selected_questions)

        return selected_questions
    
    def read_answers(self):
        answers = []
        with open(self.answers_file, "r", encoding="utf-8") as answers_file:
            answer_data = answers_file.read().split("\n")
        answers = [int(answer.split(": ")[1])  for answer in answer_data]
        return answers

class QuizApp(QWidget):
    def __init__(self, questions):
        super().__init__()
        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 400, 300)
        self.questions = questions
        self.answers = answers
        self.init_ui()

        self.correct_answers = []  # Для отслеживания правильных ответов
        self.results_window = None
        

    def init_ui(self):
        self.current_question = 0
        self.score = 0

        self.question_label = QLabel()
        self.radio_buttons = []
        self.submit_button = QPushButton('Ответить')
        self.submit_button.setEnabled(False)

        self.question_indices = list(range(len(self.questions)))

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for _ in range(len(self.questions[0]["options"])):
            radio_button = QRadioButton()
            radio_button.toggled.connect(self.enable_submit)
            self.radio_buttons.append(radio_button)
            layout.addWidget(radio_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.submit_button.clicked.connect(self.check_answer)
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]

            options = question["options"]

            self.question_label.setText(f' {question["question"]}')

            for i, radio_button in enumerate(self.radio_buttons):
                if i < len(options):
                    radio_button.setText(options[i])
                    radio_button.setChecked(False)
                    radio_button.setVisible(True)
                else:
                    radio_button.setVisible(False)

            self.submit_button.setEnabled(False)
        else:
            self.show_result()

    def enable_submit(self):
        self.submit_button.setEnabled(True)

    def check_answer(self):
        selected_option = None
        for i, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                selected_option = i+1
        
        

        correct_answer = self.answers[self.current_question]   # Получить правильный ответ из списка
        print("Правильный ответ: ",correct_answer)
        print("Выбранный ответ: ",selected_option)
        is_correct = (selected_option +1 == correct_answer)
        self.correct_answers.append(is_correct)

        self.current_question += 1

        if self.current_question == len(self.questions):
            self.show_result()
        else:
            self.show_question()

        self.update_score()


    def update_score(self):
        correct_count = sum(self.correct_answers)
        self.score = correct_count

    def show_result(self):
        result_message = 'Результаты:\n\n'
        for i, (question, is_correct) in enumerate(zip(self.questions, self.correct_answers)):
            result_message += f'Вопрос {i + 1}: {question["question"]}\n'
            if is_correct:
                result_message += 'Ответ: Правильно\n\n'
            else:
                correct_answer_index = question["correct_answer"]
                if 0 <= correct_answer_index < len(question["options"]):
                    result_message += f'Ответ: Неправильно\n'
                    result_message += f'Правильный ответ: {question["options"][correct_answer_index]}\n\n'
                else:
                    result_message += 'Ответ: Неправильно\n'
                    result_message += 'Правильный ответ: Отсутствует в вариантах ответов\n\n'

        if self.results_window is None:
            self.results_window = ResultsWindow(result_message)
            self.results_window.show()
        else:
            self.results_window.append_results(result_message)


class ResultsWindow(QWidget):
    def __init__(self, initial_results):
        super(ResultsWindow, self).__init__()
        self.setWindowTitle('Результаты')
        self.setGeometry(200, 200, 400, 600)
        self.results_text = QTextBrowser()
        self.results_text.setPlainText(initial_results)

        layout = QVBoxLayout()
        layout.addWidget(self.results_text)
        self.setLayout(layout)


    def append_results(self, result_message):
        current_text = self.results_text.toPlainText()
        self.results_text.setPlainText(current_text + result_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser = QuestionParser("vopros.txt", "answers.txt")
    questions = parser.read_questions_and_answers()
    answers = parser.read_answers()
    ex = QuizApp(questions)
    ex.answers = answers  # Добавьте атрибут answers после инициализации
    ex.show()
    sys.exit(app.exec_())
