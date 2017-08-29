#！/usr/bin/env python
#coding:utf-8
__author__ = 'caryr'
from django.conf.urls import url
from . import views

app_name = 'face'
urlpatterns = [
    url(r'^login',views.LoginUser,name='login'),
    url(r'^about', views.About, name='about'),
    url(r'^logout', views.LogoutUser, name='logouturl'),
    url(r'^changepwd',views.ChangePassword, name='changepasswordurl'),
    url(r'^add', views.AddUser, name='adduserurl'),
    url(r'^terminal_svr', views.terminal_svr, name='terminal_svr'),
    url(r'^flush', views.flush, name='flush'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # # ?P<question_id> defines the name that will be used to identify the matched pattern;
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # <li><a href="{% url 'detail' question.id %}">{{question.question_text}}</a></li> 通过name来控制
    # url(r'^(?P<question_id>[0-9]+)/result/$', views.results, name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # url(r'^homepage',views.home,name='home'),
    # url(r'^ci',views.ci,name='ci'),
    # url(r'^jp', views.jp, name='jp'),
    # url(r'^calc',views.test_all_dir_case,name='calc'),
    # #url(r'^uploadfile',views.uploadfile,name='uploadfile'),
]
