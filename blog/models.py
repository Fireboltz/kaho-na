from django.db import models
from django.contrib.auth.models import User
from datetime import date
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
