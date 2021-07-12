from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

from storages.backends.s3boto3 import S3Boto3Storage

from cuser.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)             # Mant-to-one relation (one user can have many posts, but one post will have only one user.)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    img = models.ImageField(storage=S3Boto3Storage(bucket_name='bookstore-post-images', region_name='us-east-2'))
    timestamp = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"postid":self.id})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comment_post')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comment_user')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='replies', on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    liked = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return self.comment_text
