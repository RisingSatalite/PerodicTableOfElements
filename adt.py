class Questions:
    def __init__(self, question, answer):
        self._question = question
        self.__answer = answer

    def get_question(self):
        return self._question
    
    def get_answer(self):
        return self.__answer
    
    def check_answer(self, answer):
        return (self.__answer == answer)

class Quizess:
    def __init__(self):
        self.__questions = []
        self.__questions.append(Questions("2+2",4))
        self.__questions.append(Questions("3+1",4))
        self.__questions.append(Questions("1-1",0))


    def get_questions(self):
        questionList = []
        for question in self.__questions:
            questionList.append(question.get_question())
        return questionList
    
    def check_answers(self, answers):
        correct = 0
        question_count = 0
        for question, answer in zip(self.__questions, answers):
            question_count += 1
            if question.check_answer(answer):
                correct += 1
        return correct, question_count


if(__name__ == "__main__"):
    quiz = Quizess()
    for i in quiz.get_questions():
        print(i)
    print(quiz.check_answers([4,4,4]))

    print(quiz.check_answers([0,0,4]))

    print(quiz.check_answers([4,4,0]))
