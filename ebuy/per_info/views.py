from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.template import loader ,Context
from django.http import HttpResponse
import os, time
from reg_login import models

# Create your views here.


def test(request):
    user_one = models.User.objects.filter(pk='18829035792')
    user_one = user_one[0]
    p = user_one.user_verify.all()
    if not p:
        p = 'nothing'

    return render(request, 'templates/per_info/index.html', {'user_one': user_one, 'p': p})


def info_main(request):
    return render(request, 'templates/per_info/info_main.html')


def show_info(request):
    is_login = request.session.get('is_login', None)
    if not is_login:
        return redirect('reg_login:login')
    user_phone = request.session.get("user_phone", None)
    user = models.User.objects.filter(pk=user_phone)
    user = user[0]
    return render(request, 'templates/per_info/show_info.html', {'user': user})


def modify_info(request):
    if request.method == 'GET':
        return redirect('reg_login:index')
    if request.method == 'POST':
        flag = 0
        user_phone = request.session.get("user_phone", None)
        if user_phone:
            user = models.User.objects.filter(pk=user_phone)
            user = user[0]
            user.user_nickname = request.POST.get('user_nickname')
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

            if flag != 0:
                return HttpResponse('error')
            else:
                user.save()
                return redirect('per_info:show_info')
        else:
            return redirect('reg_login:index')


def modify_pwd(request):
    return render(request, 'templates/per_info/secure_change_pwd1.html')


def handle_page_one(request):
    if request.method == 'GET':
        return redirect('per_info:modify_pwd')
    flag = 0
    if request.method == 'POST':
        user_phone = request.POST.get('phone')
        user = models.User.objects.filter(pk=user_phone)
        if not user:
            flag += 2
            return render(request, 'templates/per_info/secure_change_pwd1.html', {'flag': flag})
        else:
            user = user[0]
            questions = user.user_verify.all()
            questions_show = []
            for question in questions:
                questions_show.append(question.user_verify_question)
            return render(request, 'templates/per_info/secure_change_pwd2.html', {'phone': user.user_phone, 'questions': questions_show})
    else:
        flag += 1
        return render(request, 'templates/per_info/secure_change_pwd1.html', {'flag': flag})


def handle_page_two(request, phone_number):
    if request.method == 'GET':
        return redirect('per_info:modify_pwd')
    if request.method == 'POST':
        user = models.User.objects.filter(pk=phone_number)

        if not user:
            return render(request, 'templates/per_info/secure_change_pwd2.html', {'flag': 2, 'phone': phone_number})
        else:
            user = user[0]
            answer = user.user_verify.all()
            if answer[0].user_verify_question == '父亲姓名':
                answer_one = answer[0].user_verify_answer
                answer_two = answer[1].user_verify_answer
            else:
                answer_one = answer[1].user_verify_answer
                answer_two = answer[0].user_verify_answer
            need_to_verify_one = request.POST.get('father_name')
            need_to_verify_two = request.POST.get('mother_name')
            if answer_one and answer_two:
                if answer_one == need_to_verify_one and answer_two == need_to_verify_two:
                    return render(request, 'templates/per_info/secure_change_pwd3.html', {'phone': phone_number})
                else:
                    return render(request, 'templates/per_info/secure_change_pwd2.html', {'flag': 3, 'phone': phone_number})

            return render(request, 'templates/per_info/secure_change_pwd2.html', {'flag': 3, 'phone': phone_number})
    else:
        return render(request, 'templates/per_info/secure_change_pwd2.html', {'flag': 0, 'phone': phone_number})


def handle_page_three(request, phone_number):
    if request.method == 'GET':
        return redirect('per_info:modify_pwd')
    if request.method == 'POST':
        user = models.User.objects.filter(pk=phone_number)

        if not user:
            return render(request, 'templates/per_info/secure_change_pwd3.html', {'flag': 5, 'phone': phone_number})
        else:
            user = user[0]
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 and pwd2:
                if pwd1 == pwd2:
                    user.user_password = pwd1
                    user.save()
                    return render(request, 'templates/per_info/secure_change_pwd4.html')
                else:
                    return render(request, 'templates/per_info/secure_change_pwd3.html', {'flag': 4, 'phone': phone_number})

            return render(request, 'templates/per_info/secure_change_pwd3.html', {'flag': 6, 'phone': phone_number})
    else:
        return render(request, 'templates/per_info/secure_change_pwd3.html', {'flag': 7, 'phone': phone_number})
