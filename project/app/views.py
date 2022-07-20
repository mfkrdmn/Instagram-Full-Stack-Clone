from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from itertools import chain
import random
# Create your views here.

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User Invalid')
            return redirect('/login/')
    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is Already Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is Already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/login/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
    else:
        return render(request, 'register.html')

@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")

    else:
        return redirect("/")


@login_required(login_url='/login/')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    

    return render(request, "home.html")