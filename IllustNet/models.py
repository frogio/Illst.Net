from django.db import models
from django.contrib.auth.models import AbstractUser
from hitcount.models import HitCountMixin
# Create your models here.


class IllustNetUser(AbstractUser):
	nickname = models.CharField(max_length=100)
	introduce = models.TextField()  # 길이 제한이 없는 문자열
	profile_img_url = models.ImageField(upload_to = "profile_img/", null=True, blank=True, verbose_name=(''))
	banner_img_url = models.ImageField(upload_to = "banner_img/", null=True, blank=True, verbose_name=(''))
	follower = models.ManyToManyField('self')

class IllustPost(models.Model, HitCountMixin):
	illustrator = models.ForeignKey(IllustNetUser, on_delete=models.CASCADE, related_name='illustrator')
	recommend = models.ManyToManyField(IllustNetUser, related_name='recommend_user')
	upload_time = models.DateTimeField('생성일')
	title = models.CharField(max_length=300, null=True, default='', verbose_name=('제목'))
	brief_comment = models.TextField(verbose_name=('일러스트에 대한 설명'))
	illust_url = models.ImageField(upload_to = "images/", null=True, blank=True, verbose_name=(''))
	

class Comment(models.Model):
	comment_writer = models.ForeignKey(IllustNetUser, on_delete=models.CASCADE)
	illust = models.ForeignKey(IllustPost, null=True, default='', on_delete=models.CASCADE)
	comment = models.CharField(max_length=300)
	upload_time = models.DateTimeField('생성일')