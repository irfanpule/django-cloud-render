from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('render-log/<str:id>', views.GetRenderLog.as_view(), name='render_log'),
    path('get-session/', views.GetSessionAPIView.as_view(), name='get_session'),
    path('upload-file/', views.UploadFileAPIView.as_view(), name='upload_file'),
    path('render/', views.RenderAPIView.as_view(), name='pre_render'),
]
