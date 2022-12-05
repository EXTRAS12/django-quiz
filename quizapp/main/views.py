from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import QuizCategory, QUser


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(QuizCategory, pk=quiz_id)
    question = quiz.category.first()
    return redirect(reverse_lazy("display_quest", kwargs={"quiz_id": quiz_id, "quest_id": question.pk}))


@login_required
def display_one_quest(request, quiz_id, quest_id):
    QuizUser, created = QUser.objects.get_or_create(user=request.user)
    quiz = get_object_or_404(QuizCategory, pk=quiz_id)
    questions = quiz.category.all()
    current, next = None, None
    for item, quest in enumerate(questions):
        if quest.pk == quest_id:
            current = quest
            if item != len(questions) - 1:
                next = questions[item + 1]
    if request.method == "POST":
        quest_pk = request.POST.get("quest_pk")
        answer_to_question = QuizUser.results.get(quest__pk=quest_pk)
        answer_pk = request.POST.get("answer_pk")

        try:
            selected_variant = answer_to_question.quest.questions.get(pk=answer_pk)
        except ObjectDoesNotExist:
            raise Http404

        QuizUser.confirm_attempt(answer_to_question, selected_variant)

        if next == None:
            return redirect("result")

        return redirect(reverse_lazy("display_quest", kwargs={"quiz_id": quiz.id, "quest_id": next.id}))

    else:
        question = QuizUser.get_new_questions()
        if question is not None:
            QuizUser.create_attempts(question)

    return render(
        request, "main/detail_quiz.html", {"quiz": quiz, "quest": current, "next": next, "question": question}
    )


@login_required
def result(request):
    users = QUser.objects.all()
    return render(request, "main/result.html", {"users": users})


class IndexView(ListView):
    model = QuizCategory
    template_name = "main/index.html"
    context_object_name = "quizzes"


class RegisterUserView(CreateView):
    model = AbstractUser
    template_name = "main/register_user.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class LoginView(LoginView):
    template_name = "main/login.html"
