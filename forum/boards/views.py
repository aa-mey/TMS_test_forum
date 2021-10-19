from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import  login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls.base import reverse
from .models import Board, Topic, Post
from .forms import BoardForm, SubjectForm, NewMessageForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, id_board):
    try:
        board = Board.objects.get(id=id_board)
        topics = Topic.objects.filter(board=id_board)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board, 'topics':topics})

def single_topic(request, id_board, id_topic):  
    try:
        board = Board.objects.get(id=id_board)
        topic = Topic.objects.get(id=id_topic)
        pined_post = Post.objects.filter(topic_id=id_topic, is_parent=True).get()
        posts = Post.objects.filter(topic_id=id_topic, is_parent=False)
    except Post.DoesNotExist:
        raise Http404
    return render(request, 'view_topic.html', {'board': board, 'topic':topic, 'pined_post':pined_post, 'posts':posts})

@login_required(login_url="login")
def new_message(request, id_board, id_topic):
    board = Board.objects.get(id=id_board)
    topic = Topic.objects.get(id=id_topic)
    pined_post = Post.objects.filter(topic_id=id_topic, is_parent=True).get()
    posts = Post.objects.filter(topic_id=id_topic, is_parent=False)
    print(board, topic, pined_post, posts)
    if request.method == 'POST':
        comment_form = NewMessageForm(request.POST)
        if comment_form.is_valid():
            new_comment = Post.objects.create(
                message=comment_form.cleaned_data.get('message'),
                topic=topic,
                post_by=request.user,
                is_parent=False,
                )
            print(new_comment)
            return redirect('view_topic', id_board=board.id, id_topic=topic.id)
    else:
        comment_form = NewMessageForm()
    return render(request, 'base_template/add_message_to_topic.html', {'board': board, 'topic':topic, 'pined_post':pined_post, 'posts':posts})

@login_required(login_url="login")
def new_board(request):
    user = request.user
    context = {"board_form": BoardForm()}
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        print(board_form)
        if board_form.is_valid():
            new_board = board_form.save(commit=False)  
            new_board.user_create = user
            new_board.save()
            return redirect('board_topics', id_board=new_board.id)
        else:
            context["board_form"] = board_form
    return render(request, 'new_board.html', context)

@login_required(login_url="login")
def new_topic(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    user = request.user 
    context = {"board": board, "subject_f": SubjectForm(), "message_f": NewMessageForm()}
    if request.method == 'POST':
        subject_f = SubjectForm(request.POST)
        message_f = NewMessageForm(request.POST)
        if subject_f.is_valid() and message_f.is_valid():
            topic = Topic.objects.create(
                subject=subject_f.cleaned_data.get('subject'),
                board=board,
                user_create=user
                )
            post = Post.objects.create(
                message=message_f.cleaned_data.get('message'),
                topic=topic,
                post_by=user,
                is_parent=True,
                )
            return redirect('view_topic', id_board=board.id, id_topic=topic.id)
        else:
            context['subject_f'] = subject_f
            context['message_f'] = message_f
            context['board'] = board
    return render(request, 'new_topic.html', context)


def sign_up(request):
    return render(request, 'signup.html', {})

# def show_post(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     count = post.topic.posts.filter(created__lt=post.created).count() + 1
#     page = math.ceil(count / float(forum_settings.TOPIC_PAGE_SIZE))
#     url = '%s?page=%d#post-%d' % (reverse('djangobb:topic', args=[post.topic.id]), page, post.id)
#     return HttpResponseRedirect(url)