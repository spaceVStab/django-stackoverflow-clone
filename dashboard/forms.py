from django import forms
from . import models

class CreateQuestion(forms.ModelForm):
    class Meta:
        model = models.Questions
        fields = ['ques_title', 'ques_text']
        # fields = ['title', 'body', 'slug', 'thumb',]

class CreateAnswer(forms.ModelForm):
    class Meta:
        model = models.Answers
        fields = ['ans_text']
