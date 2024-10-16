from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('analyse', views.analyse, name='analyse'),
    path('audio/<str:filename>/', views.serve_audio, name='serve_audio'),
    

]