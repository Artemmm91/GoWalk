import os
from string import ascii_letters, digits
from math import ceil
from random import random

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from voteapp.forms import AddWalkForm, AuthForm, SignUpForm, RecoverForm, CommentForm
from voteapp.models import Poll, Option, Vote, Tag, Comment


def byRatekey(poll):
    return poll[4]


def randomOrder_key(element):
    return random()


def index(request):
    return render (request, 'index.html', {})


def rand_shuffle(request):
    context = {}
    votings = Poll.objects.filter(is_deleted=False, is_active=True)
    context['polls'] = [(item.id, item.name, item.text[:34]+'...', item.user) for item in votings]
    context['polls'] = sorted(context['polls'], key=randomOrder_key)
    return render(request, 'random.html', context)


def top(request):
    context = {}
    votings = Poll.objects.filter(is_deleted=False, is_active=True)
    context['polls'] = [(item.id, item.name, item.text[:34]+'...', item.user, item.rate) for item in votings]
    context['polls'] = sorted(context['polls'], key=byRatekey, reverse=True)
    return render(request, 'top.html', context)


@login_required
def add_voting(request):
    context = {'user': request.user}
    if request.POST:
        form = AddWalkForm(request.POST)
        if form.is_valid():
            p = Poll(name=form.data['name'], text=form.data['text'], user=request.user,
                     link=form.data['link'], is_active=True)
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
def show_voting(request, poll_id):
    context = {'id': poll_id, }
    poll = Poll.objects.get(id=poll_id)
    if poll:
        context['poll'] = poll
        is_voted = Vote.objects.filter(user=request.user, poll=poll).first() or poll.user == request.user
        context['options'] = Option.objects.filter(voting=poll)
        if is_voted:
            context['is_voted'] = True
            all = Vote.objects.filter(poll=poll).count()
            if all:
                percent = []
                for option in context['options']:
                    res = Vote.objects.filter(option=option).count() / float(all)
                    res *= 100
                    res = int(ceil(res)) if res / 1 >= 0.5 else int(res)
                    percent.append(res)
            else:
                percent = [0 for _ in context['options']]
            context['options'] = zip(context['options'], percent)
            context['like'] = poll.rate
            context['number_votes'] = all
    else:
        context['error'] = True
    context['user'] = request.user
    comments = Comment.objects.filter(poll=poll)
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
            p = Comment(text=form.data['text'], user=request.user, poll=poll)
            p.save()
            return redirect('/show/{}'.format(poll_id))
        else:
            context['errors'] = form.errors
            return redirect('/show/{}'.format(poll_id))
    else:
        form = CommentForm()
        context['add_form'] = form
        return render(request, 'show_trail.html', context)


@login_required
def delete_poll(request, poll_id):
    poll = Poll.objects.filter(id=poll_id).first()
    if request.user == poll.user or request.user.is_superuser:
        poll.is_deleted = True
        poll.save()
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
        voting = (Poll.objects.filter(user=request.user, is_deleted=False))
        context['username'] = request.user.username
        context['user_created_polls'] = [
            (
                item.id,
                item.name
            ) for item in voting
        ]
        return render(request, 'user_profile.html', context)


def all_are_in(tags, poll):
    for tag in tags:
        suitable_to_cur = Poll.objects.filter(tag=tag)
        print("---", suitable_to_cur, "---", end='\n')
        if poll not in suitable_to_cur or not tags:
            return False
    return True


def show_answer(request):
    context = {}
    votings = Poll.objects.filter(is_active=True, is_deleted=False)
    s = request.GET['quest']
    a = s.split('#')
    text = a[1:]
    if len(a) > 1:
        a[0] = a[0][:a[0].find(' ')]
    written_tags = Tag.objects.filter(text__in=text)
    context['search'] = s
    context['suitable_pools'] = []
    for item in votings:
        if (a[0] in item.user.username or a[0] in item.name or a[0] in item.text) \
                and (all_are_in(written_tags, item)) and a[0]:
            context['suitable_pools'].append((item.id, item.name))
    return render(request, 'search_answer.html', context)


@login_required
def vote(request, poll_id):
    if request.method == 'POST':
        poll = Poll.objects.get(id=poll_id)
        for opt in dict(request.POST)['option']:
            option = Option.objects.get(id=opt)
            vote = Vote(user=request.user, option=option, poll=poll)
            vote.save()
            all = Vote.objects.filter(poll=poll).count()
            if option.text == 'Like':
                res = Vote.objects.filter(option=option).count() / float(all)
                res *= 100
                res = int(ceil(res)) if res / 1 >= 0.5 else int(res)
                poll.rate = res
                poll.save()
        return redirect('/show/{}'.format(poll_id))
    else:
        return redirect('/')
