alfavit = "ABCDEFGHIJKLMNOPQRSTUVWXYZБГДЁЖЗИЙЛПУФЦЧШЩЪЫЬЭЮЯ"
chisla = "1234567890"
sim = ",.-/+_()&^%$#@!?><\""
def CodeEncode(text: str, k: int):
    # добавляем в алфавит маленькие буквы
    fullAlfavit = alfavit + alfavit.lower() + chisla + sim
    letterQty = len(fullAlfavit)
    retVal = ""
    for item in text:
        index = fullAlfavit.find(item)
        if item not in fullAlfavit:
            retVal += item
        else:
            codeIndex = (letterQty + index + k) % letterQty
            retVal += fullAlfavit[codeIndex]

    return retVal

if __name__ == '__main__':
    # Чтение вопросов из файла
    with open("vopros.txt", "r", encoding="utf-8") as file:
        voprosy = file.read()

    with open("answers.txt", "r", encoding="utf-8") as file:
        answersy = file.read()

    key = 2
    encryptedQuestions = CodeEncode(voprosy, key)
    ncryptedQuestions = CodeEncode(answersy, key)

    # Запись зашифрованных вопросов в файл "newshifr.txt"
    with open("newshifr.txt", "w", encoding="utf-8") as file:
        file.write(encryptedQuestions)


    with open("shifr_answers.txt", "w", encoding="utf-8") as file:
        file.write(ncryptedQuestions)

