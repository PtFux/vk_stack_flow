from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_page, name='main'),
    path('hot/', views.get_hot, name='hot'),
    path('tag/<str:tag_id>/', views.get_tag, name='tag'),
    path('question/<int:question_id>/', views.get_question, name='question'),
    path('login/', views.login, name='login'),
    path('logout/<path:url>', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('profile/edit/', views.get_settings, name='settings'),
    path('member/<int:user_id>', views.get_member, name='member')
]
