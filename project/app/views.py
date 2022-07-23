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
    user_followers_name = FollowersCount.objects.filter(user=pk)

    user_following = len(FollowersCount.objects.filter(follower=pk))
    user_following_name = FollowersCount.objects.filter(follower=pk)

    yeni= Profile.objects.all()

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'user_followers_name' : user_followers_name,
        'user_following_name' : user_following_name,
        "yeni" : yeni
    }

    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def home(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    yeni= Profile.objects.all()
    begen = LikePost.objects.all()
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames).union(Post.objects.filter(user = request.user))
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts

    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    context ={
            'user_profile': user_profile,
            'posts':feed_list,"yeni":yeni,"begen":begen,
            'suggestions_username_profile_list': suggestions_username_profile_list[:4]
    }


    return render(request, 'home.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        print(user,follower)

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')   

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id = post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()

        return redirect ("/")

    else: #user already liked the post
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect ("/")

@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get("image") == None:
                image = user_profile.profileimg
                bio = request.POST["bio"]
                location = request.POST["location"]
                fullName = request.POST["fullName"]

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.fullName = fullName
                user_profile.save()

        if request.FILES.get("image") != None:
                image = request.FILES.get("image")
                bio = request.POST["bio"]
                location = request.POST["location"]
                fullName = request.POST["fullName"]

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.fullName = fullName
                user_profile.save()

        return redirect("home")

    return render(request, "setting.html", {"user_profile" : user_profile})

@login_required(login_url='signin')
def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/profile/'+user)

    else:
        return redirect("/")

@login_required(login_url='signin')
def comment(request):

    user_comment = Comment.objects.all()

    if request.method == "POST":

        comment = request.POST["comment"]

        post = request.POST["idbilgisi"]
      
        z = Comment.objects.create(user = request.user, comment = comment, post_id = post )

        return redirect("/")

    return render(request, "home.html", {"user_comment" : user_comment, "z" : z})