from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_page, kwargs={'number': 1}, name='main'),
    path('pages/<int:number>/', views.get_page, name='page'),
    path('hot/<int:number>/', views.get_hot, name='hot'),
    path('tag/<str:tag_id>/', views.get_tag, name='tag'),
    path('question/<int:question_id>', views.get_question, name='question'),
    path('login/', views.get_login, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('ask/', views.get_ask, name='ask'),
    path('settings/', views.get_settings, name='settings'),
    path('member/<int:user_id>', views.get_member, name='member')
]
