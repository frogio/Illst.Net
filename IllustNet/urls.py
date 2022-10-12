from django.urls import path
from .views import main_views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'IllustNet'		# 네임 스페이스

urlpatterns = [
	path('', main_views.index, name='index'),
	#path('<int:pk>/', '' , name='detail'),
	path('illust/upload/', main_views.IllustUploadView.as_view() ,name='illust_upload'),
	#path('illust/upload/<int:pk>', '' ,name='illust_show'),
	#path('illust/upload/<int:pk>', '' ,name='illust_delete'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#	path('question/create/', question_views.QuestionCreateView.as_view(), name='question_create'),
#	path('question/modify/<int:pk>/', question_views.QuestionUpdateView.as_view(), name='question_modify'),
#	path('question/delete/<int:pk>/', question_views.QuestionDeleteView.as_view(), name='question_delete'),