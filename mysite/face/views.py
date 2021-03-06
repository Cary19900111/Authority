from mysite.common.CommonPaginator import SelfPaginator
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginUserForm,ChangePasswordForm,AddUserForm
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
import json,time,os,sys
from datetime import datetime
sys.path.append('e:\\autotest\\Authority\\mysite')
from .testcase.maintest import test_ci_all_case,test_jp_all_case
from django.http import StreamingHttpResponse
from bs4 import BeautifulSoup


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
  flag = request.POST['action']
  if(flag == 'ci'):
      return render(request, 'face/cirefresh.html')
  if(flag=='wj'):
      return render(request,'face/wjrefresh.html')
  if(flag=='jp'):
      return render(request, 'face/jprefresh.html')

@csrf_exempt
def savefile(request):
    abs_path = os.path.abspath('.')
    upload_dir = abs_path + r'\face\testcase\ci\uploadfile'
    if (request.method == "POST"):
        # save xlsx file
        myfile = request.FILES.get("myfile", None)
        if not myfile:
            return HttpResponse("No file for upload")
        destination = open(os.path.join(upload_dir, "ci.xlsx"), 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse('上传成功')
    return HttpResponse("上传失败")
@csrf_exempt
def savejpfile(request):
    abs_path = os.path.abspath('.')
    upload_dir = abs_path + r'\face\testcase\jp\uploadfile'
    if (request.method == "POST"):
        # save xlsx file
        myfile = request.FILES.get("myfile", None)
        if not myfile:
            return HttpResponse("No file for upload")
        destination = open(os.path.join(upload_dir, "jp.xlsx"), 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()
        return HttpResponse('上传成功')
    return HttpResponse("上传失败")
#跑测试
@csrf_exempt
def calc(request):
    flag = request.POST['action']
    if (flag == 'testci'):
        pic_name = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pic_name_with_suffix = r'{filename}.html'.format(filename=pic_name)
        test_ci_all_case(pic_name_with_suffix)
        #HtmlFile = r'E:\\autotest\\Authority\\mysite\\face\\testcase\\result\\{filename}'.format(filename=pic_name_with_suffix)
        resp = {'status':'200','detail':pic_name}
        return HttpResponse(json.dumps(resp), content_type="application/json")
        # if(os.path.exists(HtmlFile)):
        #     return render(request, HtmlFile)
    if(flag == 'testjp'):
        pic_name = datetime.now().strftime("%Y%m%d%H%M%S%f")
        pic_name_with_suffix = r'{filename}.html'.format(filename=pic_name)
        test_jp_all_case(pic_name_with_suffix)
        #HtmlFile = r'E:\\autotest\\Authority\\mysite\\face\\testcase\\result\\{filename}'.format(filename=pic_name_with_suffix)
        resp = {'status':'200','detail':pic_name}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def modify_html(html_path):
    '''修改error的展开'''
    html_file = open(html_path, 'rb+')
    html_page = html_file.read().decode("utf-8")
    html_soup = BeautifulSoup(html_page, "html.parser")
    #title_list = html_soup.find_all('title')  # 查询有几个学校
    # error_list = html_soup.find_all('tr',attrs={'class':'none'})
    # error_list = html_soup.find_all('a', attrs={'class': 'popup_link'})
    html_file.truncate()
    html_file.close()
    error_open = html_soup.find_all('div', attrs={'class': 'popup_window'})
    # error_content = html_soup.find_all('div', attrs={'class': 'popup_window'})
    error_content_and_close = html_soup.find_all('a', attrs={'onfocus': 'this.blur();'})
    float = 2.0
    for index in range(len(error_open)):
        float += 0.1
        id_expect = "div_ft" + str(float)
        href_expect = "javascript:showTestDetail('div_ft" + str(float) + "')"
        onclick_expect = "document.getElementById('div_ft" + str(float) + "').style.display = 'none'"
        # href="div_ft1.3"
        # href = "javascript:showTestDetail('div_ft1.3')"
        # onclick = "document.getElementById('div_ft1.3').style.display = 'none'"
        error_open[index]['id'] = id_expect
        error_content_and_close[index * 2]['href'] = href_expect
        error_content_and_close[index * 2 + 1]['onclick'] = onclick_expect
    html_return = html_soup.prettify()
    html_result = html_return.encode("utf-8")
    with open(html_path,  "wb") as f:
        f.write(html_result)
        f.close()

def readfile(filename):
    modify_html(filename)
    with open(filename, encoding='utf-8') as f:
        while True:
            c = f.read(512)
            if c:
                yield c
            else:
                break

@csrf_exempt
def scanci(request):
    pic_name = request.GET["action"]
    pic_name_with_suffix = r'{filename}.html'.format(filename=pic_name)
    abs_path = os.path.abspath('.')
    result_path = r'\\face\\testcase\\result\\{filename}'.format(filename=pic_name_with_suffix)
    HtmlFile = abs_path+result_path
    #HtmlFile = r'E:\\autotest\\Authority\\mysite\\face\\testcase\\result\\{filename}'.format(filename=pic_name_with_suffix)
    response = StreamingHttpResponse(readfile(HtmlFile))
    #  response = StreamingHttpResponse(readfile(HtmlFile))
    response['Content-Type'] ='text/html;application/octet-stream;charset=UTF-8'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(pic_name_with_suffix)
    return response