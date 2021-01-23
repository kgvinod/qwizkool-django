from django.urls import path

from . import views

# app namespace to avoid conflict with other apps
app_name = 'quiz'

urlpatterns = [
    # ex: /quiz/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /quiz/create_quiz
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    # ex: /quiz/5/
    path('<int:quiz_id>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    # ex: /quiz/5/get_status
    path('<int:quiz_id>/get_status', views.get_status, name='get_status'),
    # ex: /quiz/5/results/
    path('<int:quiz_id>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    # ex: /quiz/5/question/5/
    path('<int:quiz_id>/question/<int:question_id>/', views.QuestionView.as_view(), name='question'),
    # ex: /quiz/5/question/5/check_answer
    path('<int:quiz_id>/question/<int:question_id>/check_answer', views.check_answer, name='check_answer'),
    # ex: /quiz/5/question/5/results
    path('<int:quiz_id>/question/<int:question_id>/choice/<int:choice_id>/results/', views.QuestionResultsView.as_view(), name='question_results'),
]