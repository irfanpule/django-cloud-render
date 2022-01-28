from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('check-auth/', views.CheckAuthAPIView.as_view(), name='check_auth'),
    path('render-log/<str:id>', views.GetRenderLog.as_view(), name='render_log'),
    path('upload-file/', views.UploadFileAPIView.as_view(), name='upload_file'),
    path('render/<str:id>', views.RenderAPIView.as_view(), name='pre_render'),
    path('project-list/', views.GetProjectsAPIView.as_view(), name='project_list'),
]
