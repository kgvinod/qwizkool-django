from qwizkoolnlp.article.Sentence import Sentence
from qwizkoolnlp.quiz.Question import Question

class Quiz:
    """
    Base Article type

    """

    def __init__(self, article, num_questions=100000):
        self.article = article
        self.questions = []
        self.num_questions = num_questions
        
        count = 0
        for sentence in article.sentences:
            if (sentence.question is not None):
                #print (sentence.question)
                self.questions.append(sentence.question)
                count += 1
                if count >= self.num_questions:
                    break

        self.correct_answers = 0
        self.wrong_answers = 0









