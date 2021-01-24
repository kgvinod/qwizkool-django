from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.urls import reverse
from django.views import generic
from django.forms.models import model_to_dict

from .models import Choice, Question, Quiz
from .tasks import QuizCreator

import time
import sys
import threading


class IndexView(generic.ListView):
    template_name = 'quiz/index.html'
    context_object_name = 'latest_quiz_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Quiz.objects.order_by('-pub_date')[:5]


def create_quiz(request):

    topic = request.POST.get('topic')
    quiz = Quiz.objects.create(title_text=topic)

    t = threading.Thread(target=QuizCreator().start, args=[quiz])
    t.setDaemon(True)
    t.start()

    context = {
        'topic': topic, 
        'quiz_id': quiz.id,      
        'first_question_id' : 1  # Will be replaced in the template code
        }   

    return render(request, 'quiz/create_quiz_progress.html', context)  


def create_quiz_old(request):
    topic = request.POST.get('topic')

    quiz_id = QuizCreator().start(topic)
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    if quiz.status_text == 'READY':
        first_question = list(quiz.question_set.all())[0] 
        context = {
            'topic': topic, 
            'quiz_id': quiz_id,
            'description' : quiz.description_text,
            'information' : "The Quiz has " + str(quiz.question_count_max) + " questions.",
            'question' : first_question               
            }

        return render(request, 'quiz/create_quiz_progress.html', context)  
    else:    
        e_str_html = quiz.status_detail_text.replace("\n", "<br />") 
        context = {
            'topic': topic, 
            'information': e_str_html,
        }
        quiz.delete()
        return render(request, 'quiz/create_quiz_fail.html', context)    

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


class QuizDetailView(generic.TemplateView):
    template_name = 'quiz/quiz_detail.html'
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add to the template context
        quiz_id = self.kwargs['quiz_id'] 
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        # Clear attemped flags
        for q in quiz.question_set.all():
            q.attempted = False
            q.save()
        
        first_question = list(quiz.question_set.all())[0]             

        context['quiz'] =  quiz
        context['question'] = first_question
        return context 


class QuestionView(generic.TemplateView):
    template_name = 'quiz/question.html'
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add to the template context
        quiz_id = self.kwargs['quiz_id'] 
        question_id = self.kwargs['question_id']   
        quiz = get_object_or_404(Quiz, pk=quiz_id)
   
        context['question'] =  get_object_or_404(Question, pk=question_id)
        context['question_number'] = quiz.get_num_attempted() + 1        
        return context  

class QuizResultsView(generic.TemplateView):
    template_name = 'quiz/quiz_results.html'
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add to the template context
        quiz_id = self.kwargs['quiz_id'] 
        quiz = get_object_or_404(Quiz, pk=quiz_id)

        total = 0
        attempted = 0
        correct = 0
        wrong = 0

        for q in quiz.question_set.all():
            total += 1
            if q.attempted:
                attempted += 1
                if q.passed:
                    correct += 1
                else:
                    wrong += 1    
            
        context.update({
            'quiz': quiz,
            'total':total,
            'attempted':attempted,
            'correct' : correct,
            'wrong':wrong,
            })            

        return context 

class QuestionResultsView(generic.TemplateView):
    template_name = 'quiz/question_results.html'
    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add to the template context
        choice_id = self.kwargs['choice_id'] 
        question_id = self.kwargs['question_id']  

        context['question'] =  get_object_or_404(Question, pk=question_id)
        context['choice'] = get_object_or_404(Choice, pk=choice_id)        
        return context        


# Get status of quiz creation
def get_status(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return JsonResponse(model_to_dict(quiz))


# Choice id arrives in the POST request
def check_answer(request, quiz_id, question_id):
    question = get_object_or_404(Question, pk=question_id)
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question form.
        return render(request, 'quiz/question.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            'question_number' : quiz.get_num_attempted() + 1
        })

    question.attempted = True    
    if selected_choice.is_correct:
        message = selected_choice.choice_text + " is the correct answer!"
        question.passed = True
    else:    
        for choice in question.choice_set.all():
            if choice.is_correct:
                correct_choice = choice
        
        message = selected_choice.choice_text + " is the wrong answer! Correct answer is " + correct_choice.choice_text 
        question.passed = False

    question.save()

    # Get the next question
    next_question = None
    for q in question.quiz.question_set.all():
        if not q.attempted:
            next_question = q
            break

    return render(request, 'quiz/question_results.html', {
        'question': question,
        'passed' : question.passed, 
        'result_message': message,
        'next_question' : next_question,
    })        
      
