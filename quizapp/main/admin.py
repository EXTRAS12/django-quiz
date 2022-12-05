from django.contrib import admin

from .forms import AnswerInlineForm
from .models import Answer, Quest, QuizCategory, QUser, Result


class AnswerAdmin(admin.StackedInline):
    model = Answer
    can_delete = False
    formset = AnswerInlineForm


class QustionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]


class ResultAdmin(admin.ModelAdmin):
    list_display = ("quest", "quiz_user", "answer", "is_true", "score")

    class Meta:
        model = Result


admin.site.register(QuizCategory)
admin.site.register(Quest, QustionAdmin)
admin.site.register(Answer)
admin.site.register(Result, ResultAdmin)
admin.site.register(QUser)
