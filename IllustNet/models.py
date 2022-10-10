from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class IllustNetUser(AbstractUser):
	nickname = models.CharField(max_length=100)
	introduce = models.TextField()  # 길이 제한이 없는 문자열
	profile_img_url = models.CharField(max_length=300)
	banner_img_url = models.CharField(max_length=300)
	follower = models.ManyToManyField('self')
