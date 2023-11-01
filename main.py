import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QMessageBox

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
        selected_questions = questions[:25]

        return selected_questions


class QuizApp(QWidget):
    def __init__(self, questions):
        super().__init__()
        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 400, 300)
        self.current_question = 0
        self.score = 0
        self.questions = questions
        self.init_ui()

    def init_ui(self):

        self.question_label = QLabel()
        self.radio_buttons = []
        self.submit_button = QPushButton('Ответить')
        self.submit_button.setEnabled(False)  # Начально 
        
        self.question_indices = list(range(len(self.questions)))
        random.shuffle(self.question_indices)
        self.current_question_number = 0

        layout = QVBoxLayout()
        layout.addWidget(self.question_label)
        for _ in range(len(self.questions[0]["options"])):
            radio_button = QRadioButton()
            radio_button.toggled.connect(self.enable_submit)
            self.radio_buttons.append(radio_button)
            layout.addWidget(radio_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.submit_button.clicked.connect(self.check_answer)  # Подключаем обработчик к кнопке "Ответить"

        self.show_question()

    

    def show_question(self):
        if self.current_question_number < 25:  # Display and score only 25 questions
            if not self.question_indices:
                self.show_result()
                return

            # Get the next random question index
            random_question_index = self.question_indices.pop()
            question = self.questions[random_question_index]

            # Display the question number and text
            self.question_label.setText(f' {question["question"]}')
            options = question["options"]
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
                selected_option = i

        correct_answer = self.questions[self.current_question]["correct_answer"]
        if selected_option == correct_answer:
            self.score += 1

        self.current_question += 1
        self.show_question()

    def show_result(self):
        QMessageBox.information(self, 'Результаты', f'Вы набрали {self.score} из {len(self.questions)} баллов.')
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    parser = QuestionParser("vopros.txt", "answers.txt")
    questions = parser.read_questions_and_answers()
    ex = QuizApp(questions)
    ex.show()
    sys.exit(app.exec_())
