from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('pre-render/', views.pre_render, name='pre_render'),
    path('rendering/', views.process_render, name='rendering'),
    path('result/', views.result_render, name='result'),
]
