""" 
Test function for Qwizkool NLP
"""

import qwizkoolnlp
from qwizkoolnlp.quiz.Question import Question
from qwizkoolnlp.article.WebArticle import WebArticle
from qwizkoolnlp.article.WikipediaArticle import WikipediaArticle
from qwizkoolnlp.quiz.Quiz import Quiz
from qwizkoolnlp.nlp.QkContext import QkContext
from qwizkoolnlp.utils.QkUtils import QkUtils
import time
import wikipedia

#first_question = Question("What is your name")
#print(first_question)

#web_article = WebArticle('capacitor', 'https://en.wikipedia.org/wiki/Capacitor')
#web_article.open()

qk_ctx = QkContext('small')

while (True):
    title = input("\nQuiz me about ['q' to exit]: ")
    if title == 'q':
        break
    wiki_article = WikipediaArticle(title, qk_ctx)

    try:
        wiki_article.open()
    except wikipedia.exceptions.PageError as err:
        print("Page Error: {0}".format(err))
        continue
    except wikipedia.exceptions.DisambiguationError as err:
        print("Disambiguation Error: {0}".format(err))
        continue

    wiki_article.parse()

    quiz = Quiz(wiki_article)
    print("The Quiz has maximum " + str(len(quiz.questions)) + " questions.")

    question_num = 1
    for question in quiz.questions:
        print(question.generate_question_str(question_num))
        message = "Select your answer [1-" + str(question.num_choices()) + "]: "
        valid_range = list(range(1, question.num_choices()+1))
        answer = QkUtils().input_number(message, valid_range)
        if question.is_correct_answer(answer):
            correct_msg = "'" + question.get_choice_from_key(answer) + "' is the CORRECT answer!\n\n"
            QkUtils().animate(correct_msg, 0.01)
            quiz.correct_answers += 1
        else:
            wrong_msg = "'" + question.get_choice_from_key(answer) + "' is the WRONG answer. Correct answer is '" + question.answer + "'.\n\n"
            QkUtils().animate(wrong_msg, 0.01) 
            quiz.wrong_answers += 1
        
        if not QkUtils().input_continue():
            break

        question_num += 1

    print("\n=================")         
    print("Your score is " + str(quiz.correct_answers) + "/" + str(quiz.correct_answers + quiz.wrong_answers))
    print("=================\n")  

