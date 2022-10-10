from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from common.forms import RegisterForm

# Create your views here.


class RegisterView(generic.CreateView):
	form_class = RegisterForm
	template_name = "common/register.html"
	success_url = reverse_lazy('index')