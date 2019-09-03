from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.template import loader ,Context
from django.http import HttpResponse
import os, time
# Create your views here.


def dispatcher(requset):
    return redirect('index/')


def index(request):
    is_login = request.session.get("is_login", None)
    if is_login:
            user_phone = request.session.get('user_phone')
            user_list = models.User.objects.filter(pk=user_phone)
            if user_list:
                response = render(request, 'templates/reg_login/index.html', {'login': 1, 'user': user_list[0], 'default_profile': 'default_profile'})
                # response.set_cookie('user_phone', user_list[0].user_phone, 259220)
                return response
    return render(request, 'templates/reg_login/index.html')


def login(request):
    return render(request, 'templates/reg_login/login.html')


def reg(request):
    return render(request, 'templates/reg_login/reg.html')


# 处理注册提交的表单
def handle_reg(request):
    if request.method == "GET":
        return redirect('reg_login:reg')
    flag = 0  # 是否错误的标志
    user = models.User()
    user.user_phone = ''
    user.user_password = ''
    user.user_nickname = ''
    user.user_pic = ''
    user_verify_one = models.Secure()
    user_verify_two = models.Secure()

    if request.method == 'POST':
        user.user_phone = request.POST.get('phone')
        user.user_password = request.POST.get('password')
        user.user_nickname = request.POST.get('nickname')
        user_verify_one.user_verify_question = '父亲姓名'
        user_verify_one.user_verify_answer = request.POST.get('father_name')
        user_verify_two.user_verify_question = '母亲姓名'
        user_verify_two.user_verify_answer = request.POST.get('mother_name')
        if user.user_phone == '' or user.user_password == '' or user.user_nickname == '' or user_verify_one.user_verify_answer == '' or user_verify_two.user_verify_answer == '':
            flag = 1
        if len(user.user_password) < 8 or len(user.user_password) > 15 :
            flag = 1
        if len(user.user_phone) != 11:
            flag = 1
        if flag != 0:
            return render(request, 'templates/reg_login/reg.html', {'flag': flag})
        userindb = models.User.objects.filter(pk=user.user_phone)
        if not userindb:
            try:
                image = request.FILES.get('upload', None)
                if image:
                    user.user_pic = str(int(time.time()*10000)) + '.jpg'
                    dist = open(os.path.join('./reg_login/static/profile/', user.user_pic), 'wb')
                    for chunk in image.chunks():
                        dist.write(chunk)
                    dist.close()
            except:
                flag = 1
        else:
            flag = 2
    if user.user_phone == '' or user.user_password == '' or user.user_nickname == '':
        flag = 1
    if len(user.user_password) < 8 or len(user.user_password) > 15:
        flag = 1
    if len(user.user_phone) != 11:
        flag = 1

    if flag != 0:
        return render(request, 'templates/reg_login/reg.html', {'flag': flag})
    else:
        user.save()
        userindb2 = models.User.objects.filter(pk=user.user_phone)
        user_verify_one.user_to = userindb2[0]
        user_verify_two.user_to = userindb2[0]
        user_verify_one.save()
        user_verify_two.save()
        return render(request, 'templates/reg_login/reg_success.html')


# 处理登录提交的表单
def handle_login(request):
        if request.method == "GET":
            return redirect('reg_login:login')
        flag = 0
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = models.User.objects.filter(pk=phone)
        if user:
            if password == user[0].user_password:
                pass
            else:
                flag = 2
        else:
            flag = 1
        if flag != 0:
            return render(request, 'templates/reg_login/login.html', {'flag': flag})
        else:
            response = render(request, 'templates/reg_login/index.html', {'login': 1, 'user': user[0], 'default_profile': 'default_profile'})
            if remember is None:
                request.session['user_phone'] = user[0].user_phone
                request.session['is_login'] = True
                request.session['remember'] = False
                request.session.set_expiry(0)
            else:
                request.session['user_phone'] = user[0].user_phone
                request.session['is_login'] = True
                request.session['remember'] = True
                # response.set_cookie('user_phone', phone, 259220)
            return response


# 处理注销操作
def logout(request):
    response = render(request, 'templates/reg_login/index.html')
    # response.delete_cookie('user_phone')
    request.session.clear()
    return response



















