from django.urls import path
from .views import main_views
from .views import comment_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'IllustNet'		# 네임 스페이스

urlpatterns = [
	path('', main_views.IllustListView.as_view(), name='index'),
	path('illust/view/<int:pk>/', main_views.IllustDetailView.as_view() , name='illust_view'),
	path('illust/upload/', main_views.IllustUploadView.as_view() ,name='illust_upload'),
	path('illust/delete/<int:pk>',main_views.IllustDeleteView.as_view(), name="illust_delete"),
	path('illust/update/<int:pk>',main_views.IllustUpdateView.as_view(), name="illust_update"),
	
	
	path('illust/like/<int:illust_id>', main_views.illust_like ,name='illust_like'),

	path('illust/comment/<int:illust_id>/', comment_views.comment_create_illust, name='comment_create_illust'),
	#path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
	#path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),



	#path('illust/<int:pk>/', main_views.QuestionDetailView.as_view(), name='detail'),
	
	#path('illust/upload/<int:pk>', '' ,name='illust_delete'),

]
#	path('question/create/', question_views.QuestionCreateView.as_view(), name='question_create'),
#	path('question/modify/<int:pk>/', question_views.QuestionUpdateView.as_view(), name='question_modify'),
#	path('question/delete/<int:pk>/', question_views.QuestionDeleteView.as_view(), name='question_delete'),