from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from ..models import IllustPost

def index(request):
	illust_post = IllustPost.objects.all()
	
	return render(request, 'illust_board.html', {'illust_post' : illust_post})
	
class IllustUploadView(LoginRequiredMixin, generic.CreateView):
	model = IllustPost
	success_url = reverse_lazy('IllustNet:index')
	template_name = "illust_template/illust_post.html"
	fields = ["illust_url" , "brief_comment" ]
	
	def form_valid(self, form):
		form.instance.upload_time = timezone.now()
		form.instance.views = 0
		form.instance.illustrator = self.request.user
		return super().form_valid(form)