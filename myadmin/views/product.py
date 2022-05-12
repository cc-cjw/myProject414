import time
from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from myadmin.models import Product, Category, Shop


# 展示
def index(request, pIndex=1):
    # 获取所有数据，不包括status为9的
    list = Product.objects.filter(status__lt=9)
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        list = list.filter(name__contains=kw)
        mywhere.append('keyword=' + kw)
    # 分页,每页5个
    p = Paginator(list, 5)
    # 最大页数
    page_num = p.num_pages
    if pIndex > page_num:
        pIndex = page_num
    elif pIndex < page_num:
        pIndex = 1
    # 当前页的数据
    page_context = p.page(pIndex)
    # 页数范围
    p_num_range = p.page_range
    for vo in list:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name
    context = {'productlist': list, 'plist': p_num_range, 'pIndex': pIndex}
    return render(request, 'myadmin/product/index.html', context)


# 加载新增数据
def add(request):
    shoplist = Shop.objects.values('id', 'name')
    context = {'shoplist': shoplist}
    return render(request, 'myadmin/product/add.html', context)


# 执行新增操作
def insert(request):
    myfile = request.FILES.get('cover_pic', None)
    if not myfile:
        return HttpResponse('没有菜品图片')
    with open('./static/uploads/product/' + myfile.name, 'wb+') as destination:
        for chunk in myfile.chunks():
            destination.write(chunk)

    ob = Product()
    ob.shop_id = request.POST['shop_id']
    ob.category_id = request.POST['category_id']
    ob.cover_pic = myfile
    ob.name = request.POST['name']
    ob.price = request.POST['price']
    ob.status = 1
    ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    context = {'info': "成功"}
    return render(request, 'myadmin/info.html', context)


# 删除
def delete(request, pid):
    ob = Product.objects.get(id=pid)
    ob.status = 9
    ob.save()
    context = {'info': '删除啊成功！'}
    return render(request, 'myadmin/info.html', context)


# 加载更新信息
def edit(request, pid):
    ob = Product.objects.get(id=pid)
    shoplist = Shop.objects.values('id', 'name')
    context = {'product': ob, 'shoplist': shoplist}
    return render(request, 'myadmin/product/edit.html', context)


# 执行更新操作
def update(request, pid):
    oldpicname = request.POST['oldpicname']
    myfile = request.FILES.get('cover_pic', None)
    if not myfile:
        myfile = oldpicname
    else:
        with open('./static/uploads/product/' + myfile.name, 'wb+') as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
    # oldpicname = request.POST['oldpicname']
    # # 判断是否有文件上传
    # myfile = request.FILES.get("cover_pic", None)
    # if not myfile:
    #     cover_pic = oldpicname
    # else:
    #     # 图片的上传处理
    #     cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
    #     destination = open("./static/uploads/product/" + cover_pic, "wb+")
    #     for chunk in myfile.chunks():  # 分块写入文件
    #         destination.write(chunk)
    #     destination.close()
    ob = Product.objects.get(id=pid)
    ob.shop_id = request.POST['shop_id']
    ob.category_id = request.POST['category_id']
    ob.cover_pic = myfile
    ob.name = request.POST['name']
    ob.price = request.POST['price']
    # ob.status = request.POST['status']
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    # 判断删除老图片
    context = {"info": "修改成功！"}
    return render(request, "myadmin/info.html", context)
