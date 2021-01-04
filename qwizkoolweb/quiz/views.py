from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question, Quiz

import qwizkoolnlp
from qwizkoolnlp.quiz.Question import Question as QuestionNLP
from qwizkoolnlp.article.WebArticle import WebArticle
from qwizkoolnlp.article.WikipediaArticle import WikipediaArticle
from qwizkoolnlp.quiz.Quiz import Quiz as QuizNLP
from qwizkoolnlp.nlp.QkContext import QkContext
from qwizkoolnlp.utils.QkUtils import QkUtils
import time
import wikipedia

def index(request):
    latest_quiz_list = Quiz.objects.order_by('-pub_date')[:5]
    context = {'latest_quiz_list': latest_quiz_list}
    return render(request, 'quiz/index.html', context)  

def create_quiz(request):
    topic = request.POST.get('topic')

    qk_ctx = QkContext('small')
    wiki_article = WikipediaArticle(topic, qk_ctx)

    try:
        wiki_article.open()
    except wikipedia.exceptions.PageError as err:
        print("Page Error: {0}".format(err))
    except wikipedia.exceptions.DisambiguationError as err:
        print("Disambiguation Error: {0}".format(err))

    wiki_article.parse()

    quiz_nlp = QuizNLP(wiki_article)
    print("The Quiz has maximum " + str(len(quiz_nlp.questions)) + " questions.")

    new_quiz = Quiz.objects.create(title_text=quiz_nlp.article.title, description_text='TBD')
    new_quiz.save()

    for question in quiz_nlp.questions:
        new_question = Question.objects.create(quiz=new_quiz, question_text=question.question_line)
        new_question.save()
        
        for choice in question.choices:
            new_choice = Choice.objects.create(question=new_question, choice_text=choice, is_correct=(question.answer==choice))
            new_choice.save()

    context = {
        'topic': topic, 
        'information' : "The Quiz has maximum " + str(len(quiz_nlp.questions)) + " questions."
        }

    return render(request, 'quiz/create_quiz.html', context)  

# Retained for showing example usage with HttpResponse
# def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

# Retained for showing example of geneting custom 404
# def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'quiz/detail.html', {'question': question})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    first_question = list(quiz.question_set.all())[0] 
    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'question' : first_question               
        })

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/quiz_results.html', {'quiz': quiz})

def question(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'quiz/question.html', {'question': question})

def question_results(request, quiz_id, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=choice_id)
    return render(request, 'quiz/question_results.html', {'question': question})

# Choice id arrives in the POST request
def check_answer(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question form.
        return render(request, 'quiz/question.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    if selected_choice.is_correct:
        message = selected_choice.choice_text + " is the correct answer!"
    else:    
        for choice in question.choice_set.all():
            if choice.is_correct:
                correct_choice = choice
        
        message = selected_choice.choice_text + " is the wrong answer! Correct answer is " + correct_choice.choice_text 
        #selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('quiz:question_results', args=(question.quiz.id, question.id, selected_choice.id, )))    
    return render(request, 'quiz/question_results.html', {
        'question': question,
        'result_message': message,
    })        
