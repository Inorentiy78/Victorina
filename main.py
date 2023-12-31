import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QTextBrowser
from PyQt5.QtGui import QFont  # Import QFont

from codirok import CodeEncode

class ResultsWindow(QWidget):
    def __init__(self, initial_results):
        super(ResultsWindow, self).__init__()
        self.setWindowTitle('Результаты')
        self.setGeometry(250, 250, 450, 600)
        self.results_text = QTextBrowser()
        self.results_text.setPlainText(initial_results)

        layout = QVBoxLayout()
        layout.addWidget(self.results_text)
        self.setLayout(layout)

    def append_results(self, result_message):
        current_text = self.results_text.toPlainText()
        self.results_text.setPlainText(current_text + result_message)


class QuizApp(QWidget):
    def read_questions_and_answers(self, questions_file, answers_file):
        questions = []
        with open(questions_file, "r", encoding="utf-8") as questions_file:
            decrypted_questions = CodeEncode(questions_file.read(), -2)
            question_data = decrypted_questions.split("---\n")

        with open(answers_file, "r", encoding="utf-8") as answers_file:
            decrypted_answers = CodeEncode(answers_file.read(), -2)
            answer_data = decrypted_answers.split("\n")
        

        if len(question_data) == len(answer_data):  
            all_index = random.sample(range(0, len(question_data)), 25)
            for i in range(25):
                try:
                    # Use CodeEncode without calling read()
                    question_lines = question_data[all_index[i]].strip().split('\n')
                    question_text = question_lines[1].strip()
                    options = [option.strip() for option in question_lines[2:]]
                    correct_answer = int(answer_data[all_index[i]].split(': ')[1])  # Предполагается, что ответы представлены в виде целых чисел

                    questions.append({
                        "question": question_text,
                        "options": options,
                        "correct_answer": correct_answer
                    })
                except Exception as e:
                    print(f"Error reading question {i + 1}: {e}")


        return questions
    
    
    
    def __init__(self, questions_file, answers_file):
        super().__init__()
        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 400, 300)
        self.questions_file = questions_file
        self.answers_file = answers_file
        self.correct_answers = []
        self.results_window = None
        self.questions = self.read_questions_and_answers(questions_file, answers_file)
                                                                        

        self.init_ui()



    def init_ui(self):
        self.current_question = 0
        self.score = 0

        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 12, QFont.Bold))  # Set bold font for the question label
        self.radio_buttons = []
        self.submit_button = QPushButton('Ответить')
        self.submit_button.setEnabled(False)
        

        self.question_indices = list(range(len(self.questions)))
        self.setStyleSheet("background-color:  blue;")  
        self.setStyleSheet("background-color: gray;")

        self.question_label = QLabel()
        self.question_label.setFont(QFont(

"Arial", 12, QFont.Bold))  # Set bold font for the question label
        self.radio_buttons = []
        self.submit_button = QPushButton('Ответить')
        self.submit_button.setEnabled(False)
        self.submit_button.setStyleSheet("background-color: black;")

        # Set the background color of the "Ответить" button to green
        self.submit_button.setStyleSheet("background-color: black;")
        self.submit_button.setStyleSheet("background-color: green;")

        self.question_indices = list(range(len(self.questions)))

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        

        layout = QVBoxLayout()

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for _ in range(4):
            radio_button = QRadioButton()
            radio_button.setStyleSheet("background-color: white;")
            radio_button.toggled.connect(self.enable_submit)
            radio_button.setFont(QFont("Arial", 12))  # Set the font for radio buttons
            self.radio_buttons.append(radio_button)
            layout.addWidget(radio_button)
        self.submit_button.setFont(QFont("Arial", 12))  # Set the font for the submit button
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.submit_button.clicked.connect(self.check_answer)
        self.show_question()

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]

            options = question["options"]

            self.question_label.setText(f'{self.current_question + 1}. {question["question"]}')

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
                selected_option = i + 1

        correct_answer = self.questions[self.current_question]["correct_answer"]
        is_correct = (selected_option == correct_answer)
        self.correct_answers.append(is_correct)
        self.current_question += 1

        if self.current_question == len(self.questions):
            self.show_result()
        else:
            self.show_question()

        self.update_score()

    def update_score(self):
        correct_count = sum(1 for is_correct in self.correct_answers if is_correct)
        self.score = correct_count

    def show_result(self):
        result_message = 'Результаты:\n\n'
        font_size = 12  # Измените этот размер на нужный вам
        font = QFont("Arial", font_size)

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

        font.setBold(False)  # Установите жирный стиль, если это также необходимо
        self.results_window = ResultsWindow(result_message)
        self.results_window.results_text.setFont(font)
        self.results_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp(questions_file="newshifr.txt", answers_file="shifr_answers.txt")
    ex.show()
    sys.exit(app.exec_())
