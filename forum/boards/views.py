from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import User
from django.urls.base import reverse
from .models import Board, Topic, Post
from .forms import BoardForm, SubjectForm, NewMessageForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        topics = Topic.objects.filter(board=pk)
        print (topics)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board, 'topics':topics})

# def single_topic(request, pk):   
#     board = Board.objects.get(pk=pk)
#     topic = Topic.objects.get(pk=pk)

#     return render(request, 'view_topic.html', {})

@login_required(login_url="login")
def new_board(request):
    user = request.user
    context = {"board_form": BoardForm()}
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            new_board = board_form.save(commit=False)  
            new_board.user_create = user
            new_board.save()
            return redirect('board_topics', pk=new_board.id)
        else:
            context["board_form"] = board_form
    return render(request, 'new_board.html', context)

#@login_required(login_url="login")
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user 
    context = {"board":board, "subject_f": SubjectForm(), "message_f": NewMessageForm()}
    if request.method == 'POST':
        subject_f = SubjectForm(request.POST)
        message_f = NewMessageForm(request.POST)
        if subject_f.is_valid() and message_f.is_valid():
            topic = Topic.objects.create(
                subject=subject_f,
                board=board,
                user_create=user
                )
            post = Post.objects.create(
                message=message_f.cleaned_data.get('message'),
                topic=topic,
                post_by=user,
                is_parent=True,
                )
            return redirect('view_topic', pk=board.id)
        else:
            context['subject_f'] = subject_f
            context['message_f'] = message_f
            context['board'] = board
    return render(request, 'new_topic.html', context)


def sign_up(request):
    return render(request, 'signup.html', {})