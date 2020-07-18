from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_profile', blank=True, null=True)
    private = models.BooleanField(default=False, verbose_name='Private Account')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username

