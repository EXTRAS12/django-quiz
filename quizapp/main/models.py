from django.contrib.auth.models import User
from django.db import models
import random


class QUser(models.Model):
    """Игрок"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(verbose_name="Количество очков", default=0, decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

    def __str__(self):
        return self.user.username

    def create_attempts(self, question):
        """Создаем попытки"""
        attempts = Result(quest=question, quiz_user=self)
        attempts.save()

    def get_new_questions(self):
        """Получаем новый вопрос"""
        answered = Result.objects.filter(quiz_user=self).values_list("quest__pk", flat=True)
        last_questions = Quest.objects.exclude(pk__in=answered)
        if not last_questions.exists():
            return None
        return random.choice(last_questions)

    def confirm_attempt(self, answer_to_question, selected_answer):
        """Подтверждаем попытку"""
        if answer_to_question.quest_id != selected_answer.quest_id:
            return

        answer_to_question.selected_answer = selected_answer
        if selected_answer.is_true is True:
            answer_to_question.is_true = True
            answer_to_question.score = selected_answer.quest.max_score
            answer_to_question.answer = selected_answer

        else:
            answer_to_question.answer = selected_answer

        answer_to_question.save()

        self.update_score()

    def update_score(self):
        """Считаем количество очков"""
        update_score = self.results.filter(is_true=True).aggregate(models.Sum("score"))["score__sum"]

        self.total_score = update_score or 0
        self.save()

    def procent(self):
        ans = Quest.objects.all().count()
        res = (self.total_score * 100) / ans
        return res


class QuizCategory(models.Model):
    """Набор тестов (Категория)"""

    name = models.CharField(max_length=100, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Quest(models.Model):
    """Вопросы"""

    ALLOWED_NUMBER_OF_ANSWERS = 1

    category = models.ForeignKey(
        QuizCategory, verbose_name="Категория", on_delete=models.CASCADE, related_name="category"
    )
    quest = models.CharField(max_length=200, verbose_name="Вопрос")
    max_score = models.DecimalField(default=1, decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateField(auto_now=True, verbose_name="Обновлён")

    def __str__(self):
        return self.quest

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    """Ответы на вопросы"""

    quest = models.ForeignKey(Quest, related_name="questions", on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, verbose_name="Вариант ответа")
    is_true = models.BooleanField(default=False, verbose_name="Правильный ответ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_at = models.DateField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = "Варианты ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.answer


class Result(models.Model):
    """Ответы пользователя"""

    quiz_user = models.ForeignKey(QUser, on_delete=models.CASCADE, related_name="results")
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    is_true = models.BooleanField(default=False, null=False)
    score = models.DecimalField(verbose_name="Оценка", max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
