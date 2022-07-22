from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
import uuid #for unique id's
from datetime import datetime

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio =  models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default="user.jpeg")
    location = models.CharField(max_length=50, blank=True)
    fullName = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self) :
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) #primary_key=True nin anlamı UUID ile oluşturulacak id ler Post a entegre
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    profileImg = models.ForeignKey(Profile, on_delete=models.CASCADE,default=1)

    def __str__(self) :
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.user

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)