from django.shortcuts import render
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..models import IllustNetUser, IllustPost

class IllustNetUserView(generic.DetailView, MultipleObjectMixin):
	model = IllustNetUser
	context_object_name = 'user'									# 디폴트 : object
	template_name = "user_page/user_page.html"
	paginate_by = 10

	def get_context_data(self, **kwargs):															# kwargs가 context 역할을 함
		illust_list = IllustPost.objects.filter(illustrator = self.get_object().id)					# 먼저 나열할 리스트를 받아온 뒤
		
		if(self.request.user.is_authenticated == True 
				and self.get_object().follower.filter(pk=self.request.user.id).exists()):			# 현재 작품이 좋아요가 눌러져 있을 경우
			kwargs['followed'] = True																# 팔로우를 True로 표시
		
		else: kwargs['followed'] = False												

		
		return super(IllustNetUserView, self).get_context_data(object_list=illust_list, **kwargs)	# IllustUserNetView에 컨텍스트로 전달한다.
		
@login_required(login_url='common:login')
def follow(request, user_id):
	user = get_object_or_404(IllustNetUser, pk=user_id)


	#query_result = request.user.follower.raw("select * from IllustNet_illustnetuser_follower")
	#for result in query_result:
	#	print(result)
	
	if(user.follower.filter(pk=request.user.id).exists()):				# voter 테이블에 추천한 기록이 존재할 경우
		user.follower.remove(request.user)								# voter 추천 기록을 지운다.	(중복 추천 방지 및 추천 취소)
		
	else:
		user.follower.add(request.user)									# 추천 기록이 없을 경우 테이블에 레코드를 삽입한다.
		
	
	return redirect('IllustNet:show_user_page', pk = user.id)
	
	
@login_required(login_url='common:login')
def modify_user_page(request):
	
	user_profile = get_object_or_404(IllustNetUser, pk=request.user.id)

	if(request.method == "POST"):
	
		nick_name = request.POST.get('nick_name')
			
		chk_nickname_duplicate = IllustNetUser.objects.filter(nickname = nick_name)

		if(chk_nickname_duplicate.exists() and user_profile.id != chk_nickname_duplicate.values()[0]['id']):
			return HttpResponse("<script>alert(\"이미 존재하는 닉네임입니다.\");history.back();</script>")	# 올리기 요청
			
		else:
			user_profile.nickname = request.POST.get('nick_name')
		
		user_profile.introduce = request.POST.get('introduce')
		
		if(request.FILES.get('profile_img') != None):
			user_profile.profile_img_url = request.FILES.get('profile_img')
		
		if(request.FILES.get('banner_img') != None):
			user_profile.banner_img_url = request.FILES.get('banner_img')
		
		print(request.FILES.get('banner_img'))

		user_profile.save()

		return redirect('IllustNet:show_user_page', pk = request.user.id)

	else:
		return render(request, 'user_page/modify_profile.html')
	