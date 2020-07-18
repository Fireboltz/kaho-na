from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='post_author', blank=True, null=True)
    date = models.DateField(default=date.today)
    pinned = models.BooleanField(default=False)
    description = RichTextField(null=True, blank=True)
    draft = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='like_post', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='like_user', blank=True, null=True)
    dateTime = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return str(self.post) + "-" + str(self.user)
