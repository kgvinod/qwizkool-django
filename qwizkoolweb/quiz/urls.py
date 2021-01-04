from django.urls import path

from . import views

# app namespace to avoid conflict with other apps
app_name = 'quiz'

urlpatterns = [
    # ex: /quiz/
    path('', views.index, name='index'),
    # ex: /quiz/create_quiz
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    # ex: /quiz/5/
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    # ex: /quiz/5/results/
    path('<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    # ex: /quiz/5/question/5/
    path('<int:quiz_id>/question/<int:question_id>/', views.question, name='question'),
    # ex: /quiz/5/question/5/check_answer
    path('<int:quiz_id>/question/<int:question_id>/check_answer', views.check_answer, name='check_answer'),
    # ex: /quiz/5/question/5/results
    path('<int:quiz_id>/question/<int:question_id>/choice/<int:choice_id>/results/', views.question_results, name='question_results'),
]