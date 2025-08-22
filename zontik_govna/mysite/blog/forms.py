from django import forms
from .models import Comment

class EmailPostForms(forms.Form):
    name = forms.CharField(max_length=25) #name people who send email
    email = forms.EmailField() # email who send email
    to = forms.EmailField() # email who receive email
    comment = forms.CharField(required=False,
                              widget=forms.Textarea) # comments kotorie bydyt paste in email (optional)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()

