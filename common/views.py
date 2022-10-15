from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from common.forms import RegisterForm
from django.http import HttpResponse
from IllustNet.models import IllustNetUser


# Create your views here.


class RegisterView(generic.CreateView):
	form_class = RegisterForm
	template_name = "common/register.html"
	success_url = reverse_lazy('index')
	
	def form_valid(self, form):
		if(IllustNetUser.objects.filter(nickname=form.instance.nickname).exists()):
				return HttpResponse("<script>alert(\"닉네임이 중복되었습니다.\");history.back();</script>");	# 올리기 요청
		
		return super().form_valid(form)