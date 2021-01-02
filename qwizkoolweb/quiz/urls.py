from django.urls import path

from . import views

# app namespace to avoid conflict with other apps
app_name = 'quiz'

urlpatterns = [
    # ex: /quiz/
    path('', views.index, name='index'),
    # ex: /quiz/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /quiz/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /quiz/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]