from django.shortcuts import render
from instaMe.models import Comment, Profile, Photo, PLike
from django.shortcuts import render_to_response
from django.contrib import auth 
from instaMe.forms import LoginForm, SignUpForm, handleUploadedFile
from instaMe.forms import EditProfileForm, ChangePasswordForm, EditPhotoForm, InstaPhotoForm, InstaCommentForm
# from core.functions import pagination, nameParser, checkURL, sendMail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth.hashers import check_password
import json
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required


from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.validators import validate_email, ValidationError


# @login_required(login_url='/login/')
# def home(request):
#     return render(request, "profile.html")

# def index(request):
#     return render(request, "base.html")
@login_required(login_url='/login/')
def feed(request):
    photo_list = Photo.objects.order_by('-data').all()
    html = 'feed.html'
    context = {'photo_list': photo_list}

    return render(request, html, context)

# def profile_view(request):
#     return render(request, "feed.html")

def login_test(request):
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
    return HttpResponseRedirect('/feed/')

@login_required(login_url='/login/')
def settings(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}
    return render(request, 'settings.html', context)

def photo(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    comment_list = photo.comment_set.all()
    context = {'photo_comment': comment_list, 'form':InstaCommentForm}
    context['photo'] = photo
    return render(request, "photo.html", context)


@login_required(login_url='/login/')
def add(request):
    context = {'form_photo': InstaPhotoForm}
    print InstaPhotoForm
    # if request.method == "POST":
    #     form = InstaPhotoForm(request.POST, request=request or None)

    #     if form.is_valid():
    #         photo = form.save()
    #         return HttpResponseRedirect('/photo/' + str(photo.id))
    #     context['form_photo'] = form

    return render(request, 'add.html', context)

def signup(request):    
    context = {'form': SignUpForm}
    # Check for auth
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = SignUpForm(request.POST, request.FILES)

            if form.is_valid():
                user = form.save()

                # Login new user
                user = authenticate(username=user.username, password=form.cleaned_data['password'])
                login(request, user)

                return HttpResponseRedirect(reverse("feed"))       # Return to index page

            # Return initial form
            context['form'] = form

        return render(request, 'newsignup.html', context)      # return this page with error message

    # If user is authenticated  
    return HttpResponseRedirect(reverse("feed"))

@login_required(login_url='/login/')
def edit_profile(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}

    if request.method == "POST":
        form = EditProfileForm(request.POST, request=request or None)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('settings'))

        context['form_edit'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))

@login_required(login_url='/login/')
def change_password(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}
    
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, request=request or None)
        
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['new_password'])
            login(request, user)
            return HttpResponseRedirect(reverse('settings'))

        context['form_password'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))

@login_required(login_url='/login/')
def edit_photo(request):
    context = {'form_edit': EditProfileForm, 'form_photo': EditPhotoForm, 'form_password': ChangePasswordForm}
    
    if request.method == "POST":
        form = EditPhotoForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            form.save()
        context['form_photo'] = form
        return render(request, 'settings.html', context)

    return HttpResponseRedirect(reverse('settings'))

@login_required(login_url='/login/')
def set_photo(request):
    context = {'form_photo': InstaPhotoForm}
    if request.method == "POST":
        form = InstaPhotoForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('feed'))
        context['form_photo'] = form
        return render(request, 'add.html', context)

    return HttpResponseRedirect(reverse('add'))

@login_required(login_url='/login/')
def comment(request):
    context = {}
    # if request.user.is_authenticated():
    form = InstaCommentForm(request.POST, request=request or None)

    if form.is_valid():
        photo_id = request.POST.get('photo_id')
        photo = Photo.objects.get(id=photo_id)
        comment = form.save(photo)

    return HttpResponseRedirect(reverse("photo", kwargs={"photo_id": request.POST.get('photo_id')}))


def profile(request, username):
    try:
        user_profile = User.objects.get(username=username)
    except User.DoesNotExist, e:
        raise Http404

    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)

# def register_user(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valod():
#             form.save()
#             return HttpResponseRedirect('/singup_success/')
#     args = {}
#     args.update(csrf(request))
#     args['form'] = UserCreationForm()
#     print args
#     return render(request, "singup.html", args)

# def register_success(request):
#     return render(request, "register_success.html")

# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)
