from mysite.common.CommonPaginator import SelfPaginator
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginUserForm,ChangePasswordForm,AddUserForm
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import json

#登录
def LoginUser(request):
    '''用户登录view'''
    #return HttpResponse("123")
    if request.user.is_authenticated():
        return render(request, 'face/test.html')

    if request.method == 'GET' and request.GET.__contains__('next'):
        next = request.GET['next']
    else:
        next = '/'
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():#通常在你调用表单的is_valid() 方法时执行
            auth.login(request, form.get_user())
            return render(request,'face/test.html')
    else:
        form = LoginUserForm(request)

    kwvars = {
        #'request':request,
        'form':form,
        #'next':next,
    }
    return render(request,'face/login.html',kwvars)
#退出
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect('/face/login')
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
#修改密码
def ChangePassword(request):
    if request.method=='POST':
        form = ChangePasswordForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return render(request,'face/test.html')
    else:
        form = ChangePasswordForm(user=request.user)

    kwvars = {
        'form':form,
        'request':request,
    }
    return render(request, 'face/password.change.html', kwvars)
#增加用户
def AddUser(request):
    if request.method=='POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect('/face/login')
    else:
        form = AddUserForm()

    kwvars = {
        'form':form,
        'request':request,
    }
    return render(request,'face/add.html',kwvars)

def About(request):
    return render(request,'face/about.html')

@csrf_exempt
def terminal_svr(request):
  # 这里利用了django自身的登陆验证系统
  if not request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))
  #doSomething to terminal svr
  a = {}
  a["result"] = "post_success"
  return HttpResponse(json.dumps(a), content_type='application/json')

def flush(request):
    pass