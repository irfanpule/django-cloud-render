from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('list', views.QuizListView.as_view(), name='list'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='detail'),
    path('question/<int:pk>/preview/', views.QuestionReviewView.as_view(), name='preview'),
    path('<int:pk>/playing/', views.playing, name='playing'),
    path('question/<int:pk>/', views.ajax_question_detail, name='ajax_question_detail'),
    path('question/<int:question_id>/<int:answer_id>', views.ajax_get_answer, name='ajax_get_answer'),
    path('complete/', views.complete_quiz_preview, name='complete_quiz_preview'),
]

