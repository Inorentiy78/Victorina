установите PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QMessageBox

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Викторина')
        self.setGeometry(100, 100, 400, 300)
        self.current_question = 0
        self.score = 0
        self.init_ui()

    def init_ui(self):
        self.questions, self.answers = self.read_questions_and_answers_from_files("vopros.txt", "answers.txt")

        self.question_label = QLabel()
        self.radio_buttons = []
        self.submit_button = QPushButton('Ответить')
        self.submit_button.setEnabled(False)  # Начально отключена

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

    def read_questions_and_answers_from_files(self, questions_filename, answers_filename):
        questions = []
        with open(questions_filename, "r", encoding="utf-8") as questions_file:
            question_data = questions_file.read().split("---\n")

        answers = {}
        with open(answers_filename, "r", encoding="utf-8") as answers_file:
            answer_data = answers_file.read().split("\n")

        for question_text, answer_line in zip(question_data, answer_data):
            question_lines = question_text.split("\n")
            question = {
                "question": question_lines[0],
                "options": question_lines[1:5],
                "correct_answer": int(answer_line.split(": ")[1])
            }
            questions.append(question)
            
        return questions, answers

    def show_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.setText(question["question"])
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

        correct_answer = self.questions[self.current_question]["correct_answer"] - 1

        if selected_option == correct_answer:
            self.score += 1

        self.current_question += 1
        self.show_question()



    def show_result(self):
        QMessageBox.information(self, 'Результаты', f'Вы набрали {self.score} из {len(self.questions)} баллов.')
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
