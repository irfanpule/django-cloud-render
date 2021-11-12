from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('render-log/<str:id>', views.render_log, name='render_log'),
]
