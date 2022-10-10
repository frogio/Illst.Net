from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from IllustNet.models import IllustNetUser


class RegisterForm(UserCreationForm):
	class Meta:
		model = IllustNetUser
		fields = ["username" , "nickname", "email" ]