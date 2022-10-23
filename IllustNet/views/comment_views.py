from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..models import IllustPost, Comment

@login_required(login_url = "common:login")
def comment_create_illust(request, illust_id):
	comment = Comment(comment = request.POST['comment'], comment_writer =  request.user, upload_time = timezone.now(), illust_id = illust_id) 
	comment.save()
	
	return redirect('IllustNet:illust_view', illust_id)


@login_required(login_url = "common:login")	
def comment_modify_illust(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	# DB에 있는 내용을 불러온 뒤

	comment.comment = request.POST['comment']
	comment.save()

	return redirect('IllustNet:illust_view', comment.illust.id)
	
@login_required(login_url = "common:login")	
def comment_delete_illust(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	comment.delete()
		# db에서 삭제한다(db에서만)
		
	return redirect('IllustNet:illust_view', comment.illust.id)
		# db에서 지워졌지만, 메모리엔 계속 남은 상태.
	
	# pybo:detail/pybo/question_id로 리다이렉트 한다.
	
	# comment.question.id는 라우트 변수명
	# 따라서 redirect 위치는 pybo:detail/3/
	# 템플릿에서는 {% url 'pybo_detail' id %}
