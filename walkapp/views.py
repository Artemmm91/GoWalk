from string import ascii_letters, digits
from math import ceil
from random import random

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from walkapp.forms import AddWalkForm, AuthForm, SignUpForm, RecoverForm, CommentForm
from walkapp.models import Walk, Option, Vote, Tag, Comment


def by_rate_key(walk):
    return walk[4]


def random_order_key(element):
    return random()


def index(request):
    return render(request, 'index.html', {})


def make_link(link):
    if link.startswith("https:"):
        return link
    if link.startswith("<iframe"):
        start_link = link.find("src") + 5
        new_link = ""
        for i in range(start_link, len(link)):
            if i == "\"":
                break
            new_link += link[i]
        return new_link
    return link


def rand_shuffle(request):
    context = {}
    this_walks = Walk.objects.filter(is_deleted=False, is_active=True)
    context['walks'] = [(item.id, item.name, item.text[:34]+'...', item.user) for item in this_walks]
    context['walks'] = sorted(context['walks'], key=random_order_key)
    return render(request, 'random.html', context)


def top(request):
    context = {}
    this_walks = Walk.objects.filter(is_deleted=False, is_active=True)
    context['walks'] = [(item.id, item.name, item.text[:34]+'...', item.user, item.rate) for item in this_walks]
    context['walks'] = sorted(context['walks'], key=by_rate_key, reverse=True)
    return render(request, 'top.html', context)


@login_required
def add_walk(request):
    context = {'user': request.user}
    if request.POST:
        form = AddWalkForm(request.POST)
        if form.is_valid():
            p = Walk(name=form.data['name'], text=form.data['text'], user=request.user,
                     link=make_link(form.data['link']), is_active=True)
            p.save()
            context['id'] = p.id
            opt_like = Option(text='Like', voting=p)
            opt_like.save()
            opt_dislike = Option(text='Dislike', voting=p)
            opt_dislike.save()
        else:
            context['errors'] = form.errors
        return render(request, 'add_result.html', context)
    else:
        form = AddWalkForm()
        context['add_form'] = form
        return render(request, 'add.html', context)


@login_required
def show_walk(request, walk_id):
    context = {'id': walk_id, }
    walk = Walk.objects.get(id=walk_id)
    if walk:
        context['walk'] = walk
        is_voted = Vote.objects.filter(user=request.user, walk=walk).first() or walk.user == request.user
        context['options'] = Option.objects.filter(voting=walk)
        if is_voted:
            context['is_voted'] = True
            all_votes = Vote.objects.filter(walk=walk).count()
            if all_votes:
                percent = []
                for option in context['options']:
                    res = Vote.objects.filter(option=option).count() / float(all_votes)
                    res *= 100
                    res = int(ceil(res)) if res / 1 >= 0.5 else int(res)
                    percent.append(res)
            else:
                percent = [0 for _ in context['options']]
            context['options'] = zip(context['options'], percent)
            context['like'] = walk.rate
            context['number_votes'] = all_votes
    else:
        context['error'] = True
    context['user'] = request.user
    comments = Comment.objects.filter(walk=walk)
    context['comments'] = [
        (
            item.user,
            item.text,
            item.datetime
        ) for item in comments
    ]
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(text=form.data['text'], user=request.user, walk=walk)
            new_comment.save()
            return redirect('/show/{}'.format(walk_id))
        else:
            context['errors'] = form.errors
            return redirect('/show/{}'.format(walk_id))
    else:
        form = CommentForm()
        context['add_form'] = form
        return render(request, 'show_trail.html', context)


@login_required
def delete_walk(request, walk_id):
    walk = Walk.objects.filter(id=walk_id).first()
    if request.user == walk.user or request.user.is_superuser:
        walk.is_deleted = True
        walk.save()
    return redirect('/')


def login_view(request):
    context = {}
    if request.POST:
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.data['username'], password=form.data['password'])
            if user is not None:
                login(request, user)
                return redirect(index)
            else:
                return redirect('/signin')
        else:
            return redirect('/signin')
    else:
        form = AuthForm()
        context['auth_form'] = form
        return render(request, 'auth.html', context)


def logout_view(request):
    logout(request)
    return redirect(index)


def add_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(index)
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_required
def change_password(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/')
        else:
            return redirect('profile/new_pass/')
    else:
        form = PasswordChangeForm(request.user)
        context['new_pass_form'] = form
    return render(request, 'new_pass.html', context)


def reset_password(request):
    context = {}
    if request.method == 'POST':
        form = RecoverForm(request.POST)
        if form.is_valid():
            name = form.data['username']
            u = User.objects.filter(username=name).first()
            if u is not None:
                new_password = User.objects.make_random_password(length=10, allowed_chars=ascii_letters + digits)
                u.set_password(new_password)
                u.save()
                message = 'Hi! Your new password is: ' + new_password
                mail = u.email
                print(message)
                send_mail('New Password', message, 'from@example.com', [mail])
                return redirect(index)
            else:
                return redirect('/')
        else:
            return redirect('signin/')
    else:
        form = RecoverForm()
        context['name_form'] = form
    return render(request, 'rec_pass.html', context)


@login_required
def user_profile(request):
    context = {}
    if request.method != 'POST':
        user_walks = (Walk.objects.filter(user=request.user, is_deleted=False))
        context['username'] = request.user.username
        context['user_created_walks'] = [
            (
                item.id,
                item.name
            ) for item in user_walks
        ]
        return render(request, 'user_profile.html', context)


def all_are_in(tags, walk):
    for tag in tags:
        suitable_to_cur = Walk.objects.filter(tag=tag)
        print("---", suitable_to_cur, "---", end='\n')
        if walk not in suitable_to_cur or not tags:
            return False
    return True


def show_answer(request):
    context = {}
    all_walks = Walk.objects.filter(is_active=True, is_deleted=False)
    s = request.GET['quest']
    a = s.split('#')
    text = a[1:]
    if len(a) > 1:
        a[0] = a[0][:a[0].find(' ')]
    written_tags = Tag.objects.filter(text__in=text)
    context['search'] = s
    context['suitable_walks'] = []
    for item in all_walks:
        if (a[0] in item.user.username or a[0] in item.name or a[0] in item.text) \
                and (all_are_in(written_tags, item)) and a[0]:
            context['suitable_walks'].append((item.id, item.name))
    return render(request, 'search_answer.html', context)


@login_required
def vote(request, walk_id):
    if request.method == 'POST':
        walk = Walk.objects.get(id=walk_id)
        for opt in dict(request.POST)['option']:
            option = Option.objects.get(id=opt)
            this_vote = Vote(user=request.user, option=option, walk=walk)
            this_vote.save()
            all_votes = Vote.objects.filter(walk=walk).count()
            if option.text == 'Like':
                result = Vote.objects.filter(option=option).count() / float(all_votes)
                result *= 100
                result = int(ceil(result)) if result / 1 >= 0.5 else int(result)
                walk.rate = result
                walk.save()
        return redirect('/show/{}'.format(walk_id))
    else:
        return redirect('/')
