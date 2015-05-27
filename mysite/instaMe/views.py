from django.shortcuts import render
from instaMe.models import Comment, Profile
from django.shortcuts import render_to_response
from django.contrib import auth 
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
import json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "login.html")

def singup(request):
    return render(request, "register.html")

def index(request):
    return render(request, "base.html")

def feed(request):
    return render(request, "feed.html")

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("newlogin.html", c)

def loggedin(request):
    return render(request, "feed.html" )

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/feed/')
    else:
        return HttpResponseRedirect('/error/')

def error(request):
    return render(request, "error.html")

def logout(request):
    auth.logout(request)
    return render(request, "newlogin.html")

def main(request):
    # Switch path
    if request.path == '/':
        comment_list = Comment.objects.order_by('-data').all()
        html = 'newlogin.html'
    elif request.path == '/instaMe/':
        comment_list = Comment.objects.order_by('-data').all()
        html = 'base.html'

    context = {'comment_list': comment_list}

    return render(request, html, context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valod():
            form.save()
            return HttpResponseRedirect('/singup_success/')
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    print args
    return render(request, "singup.html", args)

def register_success(request):
    return render(request, "register_success.html")

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
