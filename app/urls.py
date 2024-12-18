from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/edit/', views.settings, name='settings'),
    path('ask/', views.ask_question, name="ask"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>', views.question, name="question"),
    path('tag/<tag_name>', views.tag, name="tag"),
    path('logout/', views.logout, name='logout'),
    path('<int:answer_id>/vote_answer', views.vote_answer, name='vote_answer'),
    path('<int:question_id>/vote_question', views.vote_question, name='vote_question'),
    path('<int:answer_id>/set_correct', views.tick_correct, name='tick_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
