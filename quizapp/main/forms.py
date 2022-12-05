from django import forms

from .models import *


class AnswerInlineForm(forms.BaseInlineFormSet):
    def clean(self):
        super(AnswerInlineForm, self).clean()

        correct_count = 0
        for form in self.forms:
            if not form.is_valid():
                pass
            if form.cleaned_data and form.cleaned_data["is_true"] is True:
                correct_count += 1

        try:
            assert correct_count == Quest.ALLOWED_NUMBER_OF_ANSWERS
        except AssertionError:
            raise forms.ValidationError("Допускается всего один ответ!")
