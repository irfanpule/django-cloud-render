from django.urls import path, include

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.index, name='index'),
    path('pre-render/<str:id>', views.pre_render, name='pre_render'),
    path('rendering/<str:id>', views.process_render, name='rendering'),
    path('result/<str:id>', views.result_render, name='result'),
    path('download-result/<str:id>', views.download_result, name='download_result'),
    path('accounts/', include('django.contrib.auth.urls')),
]
