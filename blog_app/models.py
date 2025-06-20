from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200) # category ko name 
    field = models.CharField(max_length=100) # related topic rakna milxa 
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # CASCADE ko main use vaneko kunaii object delete vayo vane tyo releated object haru sabaii delete hunxa  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto time on post creation
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # Related post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Comment author  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # Time of comment


    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"




