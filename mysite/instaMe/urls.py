from django.conf.urls import url

from . import views

urlpatterns = [
	# ex: /polls/
	url(r'^$', views.main, name='main'),
	# ex: /polls/5/
	# url(r'^instaMe/', views.main, name='login'),
	# url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
	# ex: /polls/5/results/
	# ex: /polls/5/vote/
	# url(r'^index/$', views.index, name='vote'),

	url(r'^login/$', views.login_test, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^auth/$', views.auth_view, name='auth'),
	url(r'^feed/$', views.feed, name='feed'),
	url(r'^loggedin/$', views.loggedin, name='loggedin'),
	url(r'^error/$', views.error, name='error'),
	url(r'^signup/$', views.signup, name='singup'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
	url(r'^change_password/', views.change_password, name='change_password'),
	url(r'^edit_photo/', views.edit_photo, name='edit_photo'),
	url(r'^add/$', views.add, name='add_photo'),
	url(r'^set_photo/$', views.set_photo, name='set_photo'),
	url(r'^photo/(?P<photo_id>\d+)/$', views.photo, name='photo'),
	url(r'^comment/$', views.comment, name='comment'),
	# url(r'^singup_success/$', views.singup_success, name='singup_success'),
	url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
]