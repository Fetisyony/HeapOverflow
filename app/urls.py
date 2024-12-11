from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('ask/', views.ask_question, name="ask"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>', views.question, name="question"),
    path('tag/<tag_name>', views.tag, name="tag"),
    path('logout/', views.logout, name='logout'),
]
