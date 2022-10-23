from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from hitcount.views import HitCountDetailView
from django.db.models import Q

from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..models import IllustPost


class IllustListView(generic.ListView):
	model = IllustPost
	context_object_name = 'illust_objects'
	paginate_by = 10
	template_name = "illust_board.html"
	#ordering = ['-upload_time']
	
	def get_context_data(self, *args, **kwargs):
		# 템플릿에 넘길 context 데이터를 만들어낸다.
		context = super().get_context_data(*args, **kwargs)
		kw = self.request.GET.get('kw', '')		# 검색어
		
		context['kw'] = kw
		context['extra'] = 'kw=' + kw
		
		return context
		
	def get_queryset(self):
		kw = self.request.GET.get('kw', '')
		illust_list = IllustPost.objects.all().order_by('-upload_time')

		# 검색 키워드값에 값이 존재할 경우, 필터를 통해 조건에 맞는 내용을 가져온다.
		if(kw):
			illust_list = illust_list.filter(
			Q(title__icontains=kw) |
			Q(illustrator__nickname__icontains=kw)).distinct()

		return illust_list

	
class IllustUploadView(LoginRequiredMixin, generic.CreateView):
	model = IllustPost
	success_url = reverse_lazy('IllustNet:index')
	template_name = "illust_template/illust_post.html"
	fields = ["title", "illust_url" , "brief_comment" ]
	
	def form_valid(self, form):
	
		if(self.request.FILES.get('illust_url') == None):												# 일러스트 파일이 올려져 있지 않을 경우
			return HttpResponse("<script>alert(\"일러스트 파일을 올려주세요\");history.back();</script>")		# 올리기 요청
	
		form.instance.upload_time = timezone.now()
		form.instance.views = 0
		form.instance.illustrator = self.request.user
		return super().form_valid(form)
		
class IllustDetailView(HitCountDetailView):
	model = IllustPost
	context_object_name = 'illust'									# 디폴트 : object
	template_name = "illust_template/illust_view.html"
	count_hit = True

	def get_context_data(self, **kwargs):							# 좋아요 표시 여부를 컨텍스트에 추가
		context = super().get_context_data()
		illust = context['illust']																# 현재 사이트에서 보여지는 illust 객체를 가져온다.

#		print(illust.comment_set.all())															# 관계 매니저로 코멘트를 받아온다.

		if(self.request.user.is_authenticated == True 
						and illust.recommend.filter(pk=self.request.user.id).exists()):			# 현재 작품이 좋아요가 눌러져 있을 경우
				context['illust_is_liked'] = True												# 좋아요를 True로 표시

		else: context['illust_is_liked'] = False												# 그렇지 않을 경우 False

		return context

class IllustDeleteView(generic.DeleteView):
	model = IllustPost
	success_url = reverse_lazy('IllustNet:index')
	
	def get(self, *args, **kwargs):
		return self.delete(*args, **kwargs)
	

class IllustUpdateView(generic.UpdateView):
	model = IllustPost
	success_url = reverse_lazy('IllustNet:index')
	template_name = "illust_template/illust_post.html"
	fields = ["title", "illust_url" , "brief_comment" ]
	
	#def form_valid(self, form):
	#	#if(self.request.FILES.get('illust_url') == None):			# 일러스트 파일이 올려져 있지 않을 경우
	#	#	return HttpResponse("<script>alert(\"일러스트 파일을 올려주세요\");history.back();</script>");	# 올리기 요청
	#	return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('IllustNet:illust_view', kwargs={'pk' : self.object.pk})
		

@login_required(login_url='common:login')
def illust_like(request, illust_id):
	illust = get_object_or_404(IllustPost, pk=illust_id)

	if(illust.recommend.filter(pk=request.user.pk).exists()):			# voter 테이블에 추천한 기록이 존재할 경우
		illust.recommend.remove(request.user)							# voter 추천 기록을 지운다.	(중복 추천 방지 및 추천 취소)
	
	else:
		illust.recommend.add(request.user)								# 추천 기록이 없을 경우 테이블에 레코드를 삽입한다.

	return redirect('IllustNet:illust_view', pk = illust.id)