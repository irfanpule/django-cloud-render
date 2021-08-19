from django.urls import path
from . import views

app_name = 'missing_object'
urlpatterns = [
    path('list', views.MissingObjectListView.as_view(), name='list'),
    path('<int:pk>/', views.MissingObjectDetailView.as_view(), name='detail'),
]
