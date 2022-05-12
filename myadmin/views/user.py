import random
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
import datetime,time
# Create your views here.
from myadmin.models import User


def index(request, pIndex=1):
    list = User.objects.filter(status__lt=9)  # 获取已有的所有信息

    # 搜索框模糊查询
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        list = list.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append("keyword=" + kw)
    # 执行分页操作
    pIndex = int(pIndex)
    page = Paginator(list, 5)  # 5条一页
    p_num = page.num_pages  # 一共有多少页
    if pIndex > p_num:
        pIndex = p_num
    elif pIndex < 1:
        pIndex = 1
    page_context = page.page(pIndex)  # 获取当前页数的所有列表
    p_num_range = page.page_range  # 获取的是页码的范围  eg：输出值是range(1,3)
    context = {'userlist': page_context, "plist": p_num_range, 'pIndex': pIndex, "mywhere": kw}
    return render(request, "myadmin/user/index.html", context)


def add(request):
    return render(request, "myadmin/user/add.html")


def insert(request):
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        # 获取密码并md5
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "添加成功"}
    except Exception as e:
        print(e)
        context = {"info": "添加失败"}

    return render(request, "myadmin/info.html", context)


def delete(request, uid):
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": '删除成功'}
    except Exception as e:
        context = {"info": "删除啊失败"}
    return render(request, "mydmin/info.html", context)


def edit(request, uid):
    try:
        ob = User.objects.get(id=uid)
        context = {"user": ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as e:
        print(e)
        context = {"info": "没有找到要修改的信息"}
        return render(request, "myadmin/info.html", context)


def update(request, uid):
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": '更新成功'}
    except Exception as e:
        context = {"info": "更新失败"}
    return render(request, "myadmin/info.html", context)



