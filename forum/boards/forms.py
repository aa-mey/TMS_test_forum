from django import forms
from django.forms import ModelForm
from django.forms import fields
from boards.models import Board, Topic, Post

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ["name", "description"]

class SubjectForm(ModelForm):
    subject = forms.CharField(widget=forms.Textarea(), max_length=250)
    
    class Meta:
        model = Topic
        fields = ["subject"]

class NewMessageForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea(), max_length=4000)
    
    class Meta:
        model = Post
        fields = ["message"]