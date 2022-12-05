from django.contrib.auth import views
from django.urls import path

from .views import (
    IndexView,
    LoginView,
    RegisterUserView,
    display_one_quest,
    quiz_detail,
    result,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quiz/<int:quiz_id>', quiz_detail, name='detail_quiz'),
    path('quiz/<int:quiz_id>/quest/<int:quest_id>', display_one_quest, name="display_quest"),
    path('quiz/result/', result, name='result'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
]
