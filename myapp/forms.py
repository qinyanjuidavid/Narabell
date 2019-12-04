from django import forms
from django.forms import ModelForm
from myapp.models import Book


class BookForm(ModelForm):
    class Meta:
        model=Book
        fields=['title','author','pdf','cover']
