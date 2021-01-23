import qwizkoolnlp
from qwizkoolnlp.quiz.Question import Question as QuestionNLP
from qwizkoolnlp.article.WebArticle import WebArticle
from qwizkoolnlp.article.WikipediaArticle import WikipediaArticle
from qwizkoolnlp.quiz.Quiz import Quiz as QuizNLP
from qwizkoolnlp.nlp.QkContext import QkContext
from qwizkoolnlp.utils.QkUtils import QkUtils
import time
import wikipedia
import sys

from .models import Choice, Question, Quiz


class QuizCreator():

    def start(self, topic):

        new_quiz = Quiz.objects.create(title_text=topic)
        new_quiz.status_text = "LOADING MODELS"
        new_quiz.save()
    
        qk_ctx = QkContext('small')
        wiki_article = WikipediaArticle(topic, qk_ctx)

        new_quiz.status_text = "CRAWLING WEB"
        new_quiz.save()

        try:
            wiki_article.open()
        #except wikipedia.exceptions.PageError as err:
        #    print("Page Error: {0}".format(err))
        #    return render(request, 'quiz/create_quiz_fail.html', context)
        #except wikipedia.exceptions.DisambiguationError as err:
        #    print("Disambiguation Error: {0}".format(err))
        #    return render(request, 'quiz/create_quiz_fail.html', context)
        except: # catch *all* exceptions
            e_str = format(sys.exc_info()[1])
            new_quiz.status_text = "FAILED"
            new_quiz.status_detail_text = e_str
            new_quiz.save()
            return new_quiz.id 

        new_quiz.status_text = "PARSING WEB DATA"
        new_quiz.save()        
        wiki_article.parse()

        new_quiz.status_text = "CREATING QUIZ"
        new_quiz.save() 
        quiz_nlp = QuizNLP(wiki_article)
        print("The Quiz has " + str(len(quiz_nlp.questions)) + " questions.")

        new_quiz.description_text = quiz_nlp.article.sentences[0]
        new_quiz.question_count_max = len(quiz_nlp.questions)
        new_quiz.save()

        new_quiz.status_text = "CREATING QUESTIONS"
        new_quiz.save() 
        for question in quiz_nlp.questions:
            new_question = Question.objects.create(quiz=new_quiz, question_text=question.question_line)
            new_question.save()
            new_quiz.question_count += 1
            new_quiz.save()
            
            for choice in question.choices:
                new_choice = Choice.objects.create(question=new_question, choice_text=choice, is_correct=(question.answer==choice))
                new_choice.save()

        new_quiz.status_text = "READY"
        new_quiz.status_detail_text = ''
        new_quiz.save()
        return new_quiz.id