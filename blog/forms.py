from django import forms
from .models import Comment


# Форма отправки поста по email.
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


# Форма комментариев.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# Форма поиска.
class SearchForm(forms.Form):
    query = forms.CharField()