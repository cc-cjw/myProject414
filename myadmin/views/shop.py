import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from myadmin.models import Shop


# 浏览店铺信息
def index(request, pIndex=1):
    # 查询已经过滤状态为9的所有的店铺信息
    list = Shop.objects.filter(status__lt=9).order_by('name')
    # 做模糊查询
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)
    # 做分页处理
    p = Paginator(list, 5)  # 每页5个
    p_num = p.num_pages  # 最大页数
    if pIndex > p_num:
        pIndex = p_num
    elif pIndex < p_num:
        pIndex = 1
    # 获取当前页面的数据
    p_context = p.page(pIndex)
    # 获取页码范围
    p_num_range = p.page_range

    context = {"shoplist": p_context, 'plist': p_num_range, 'pIndex': pIndex, 'mywhere': kw}
    return render(request, 'myadmin/shop/index.html', context)


# 加载店铺信息
def add(request):
    return render(request, 'myadmin/shop/add.html')


# 执行加载操作
def insert(request):
    # try:
    myfile = request.FILES.get('cover_pic', None)
    if not myfile:
        return HttpResponse('没有封面图片')
    with open('./static/uploads/shop/' + myfile.name, 'wb+') as destination:
        for chunk in myfile.chunks():
            destination.write(chunk)

    myfile1 = request.FILES.get('banner_pic', None)
    if not myfile1:
        return HttpResponse('没有logo')
    with open('./static/uploads/shop/' + myfile1.name, 'wb+') as destination:
        for chunk in myfile1.chunks():
            destination.write(chunk)

    # 实例化model，封装信息，并执行添加
    ob = Shop()
    ob.name = request.POST['name']
    ob.phone = request.POST['phone']
    ob.address = request.POST['address']
    ob.status = 1
    ob.cover_pic = myfile.name
    ob.banner_pic = myfile1.name
    ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    context = {'info': '店铺添加成功！'}
    # except Exception as e:
    #     print(f"错误信息------{e}")
    #     context = {'info': '店铺添加失败！'}
    return render(request, 'myadmin/info.html', context)


# 删除店铺信息
def delete(request, sid):
    ob = Shop.objects.get(id=sid)
    ob.status = 9
    ob.save()
    context = {'info': '删除成功！'}
    return render(request, 'myadmin/info.html', context)


# 编辑店铺信息
def edit(request, sid):
    ob = Shop.objects.get(id=sid)
    context = {'shop': ob}
    return render(request, 'myadmin/shop/edit.html', context)


# 执行更新操作
def update(request, sid):
    oldpicname = request.POST['oldpicname']
    myfile = request.FILES.get('cover_pic', None)
    if not myfile:
        myfile = oldpicname
    else:
        with open('./static/uploads/product/' + myfile.name, 'wb+') as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)

    oldpicname1 = request.POST['oldpicname1']
    myfile1 = request.FILES.get('banner_pic', None)
    if not myfile1:
        myfile1 = oldpicname1
    else:
        with open('./static/uploads/shop/' + myfile1.name, 'wb+') as destination:
            for chunk in myfile1.chunks():
                destination.write(chunk)
    ob = Shop.objects.get(id=sid)
    ob.name = request.POST['name']
    ob.phone = request.POST['phone']
    ob.address = request.POST['address']
    ob.status = request.POST['status']
    ob.cover_pic = myfile
    ob.banner_pic = myfile1
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    context = {'info': '更新店铺信息成功！'}
    return render(request, 'myadmin/info.html', context)
