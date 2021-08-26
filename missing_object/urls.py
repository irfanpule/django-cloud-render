from django.urls import path
from . import views

app_name = 'missing_object'
urlpatterns = [
    path('list', views.MissingObjectListView.as_view(), name='list'),
    path('<int:pk>/', views.MissingObjectDetailView.as_view(), name='detail'),
    path('<int:pk>/preview/', views.QuestionReviewView.as_view(), name='preview'),
    path('<int:pk>/playing/', views.playing, name='playing'),
    path('get-pictures/', views.ajax_get_pictures, name='ajax_get_pictures'),
    path('<int:id>/get-answer/', views.ajax_get_answer, name='ajax_get_answer'),
]
