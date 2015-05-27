from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /polls/
	url(r'^$', views.main, name='base'),
	# ex: /polls/5/
	url(r'^instaMe/', views.main, name='login'),
	# url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /polls/5/results/
	# ex: /polls/5/vote/
	url(r'^index/$', views.index, name='vote'),

	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^auth/$', views.auth_view, name='auth'),
	url(r'^feed/$', views.feed, name='feed'),
	url(r'^loggedin/$', views.loggedin, name='loggedin'),
	url(r'^error/$', views.error, name='error'),
	url(r'^singup/$', views.singup, name='singup'),
	url(r'^singup_success/$', views.singup_success, name='singup_success'),
]