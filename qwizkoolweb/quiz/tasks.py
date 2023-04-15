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
from background_task import background
from .models import Choice, Question, Quiz
import threading



class QuizCreator():

    def start(self, quiz_id):
        
        new_quiz = Quiz.objects.get(pk=quiz_id)

        new_quiz.status_text = "Loading Models"
        new_quiz.save(update_fields=["status_text"])
        qk_ctx = QkContext('small')


        new_quiz.status_text = "Crawling Web"
        new_quiz.save(update_fields=["status_text"])

        wiki_article = WikipediaArticle(new_quiz.title_text, qk_ctx)
        try:
            new_quiz.title_text = wiki_article.open()
        except: # catch *all* exceptions
            e_str = format(sys.exc_info()[1])
            new_quiz.status_text = "FAILED"
            new_quiz.status_detail_text = e_str
            print('FAILED', e_str)
            new_quiz.save()
            return new_quiz.id 

        new_quiz.status_text = "Parsing Web Data"
        new_quiz.save(update_fields=["status_text"])
        wiki_article.parse()

        new_quiz.status_text = "Creating Quiz"
        new_quiz.save(update_fields=["status_text"])

        # Limit number of questions to 25
        quiz_nlp = QuizNLP(wiki_article, 25)
        print("The Quiz has " + str(len(quiz_nlp.questions)) + " questions.")

        new_quiz.description_text = quiz_nlp.article.sentences[0]
        new_quiz.question_count_max = len(quiz_nlp.questions)
        new_quiz.save()

        new_quiz.status_text = "Creating Questions"
        new_quiz.save(update_fields=["status_text"])
        for question in quiz_nlp.questions:
            new_question = Question.objects.create(quiz=new_quiz, question_text=question.question_line)
            new_question.save()
            new_quiz.question_count += 1
            if new_quiz.first_question_id == 0:
               new_quiz.first_question_id =  new_question.id 
            new_quiz.save()
            
            for choice in question.choices:
                new_choice = Choice.objects.create(question=new_question, choice_text=choice, is_correct=(question.answer==choice))
                new_choice.save()

        new_quiz.status_text = "READY"
        new_quiz.status_detail_text = ''
        new_quiz.save(update_fields=["status_text", "status_detail_text"])
        return new_quiz.id


@background(schedule=0)
def quiz_create_bg(quiz_id):
    t = threading.Thread(target=QuizCreator().start, args=[quiz_id])
    t.setDaemon(True)
    t.start()