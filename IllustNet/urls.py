from django.urls import path
from .views import main_views

app_name = 'IllustNet'		# 네임 스페이스

urlpatterns = [
	path('', main_views.index, name='index'),	
]