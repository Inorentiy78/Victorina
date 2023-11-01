alfavit = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ.+-/+_()&^%$#@!?><\""

def CodeEncode(text: str, k: int):
    # добавляем в алфавит маленькие буквы
    fullAlfavit = alfavit + alfavit.lower()
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
print(voprosy)

with open("shifanswers.txt", "w", encoding="utf-8") as file:
    file.write(ncryptedQuestions)
print(answersy)
