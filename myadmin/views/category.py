from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from myadmin.models import Category, Shop


# 加载信息
def index(request, pIndex=1):
    # 获取所有
    list = Category.objects.filter(status__lt=9)
    # 做模糊查询
    mywhere = []
    kw = request.GET.get('keyword', None)
    if kw:
        list = list.filter(name__contains=kw)
        mywhere.append("keyword=" + kw)
    print(f'mywhere={mywhere}')

    # 分页
    p = Paginator(list, 5)
    # 总页数
    p_num = p.num_pages
    if pIndex > p_num:
        pIndex = p_num
    elif pIndex < p_num:
        pIndex = 1
    # 当前页的内容
    page_context = p.page(pIndex)
    # 当前多少页数的范围
    p_num_range = p.page_range
    # 遍历信息，并获取对应的商铺名称，以shopname名封装
    for vo in page_context:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
    for i in page_context:
        print(f'==========={i}----{i.shopname}')
    context = {"categorylist": page_context, 'plist': p_num_range, 'pIndex': pIndex, 'mywhere': kw}
    return render(request, 'myadmin/category/index.html', context)


# 加载新增信息
def add(request):
    shoplist = Shop.objects.values("id", 'name')
    context = {"shoplist": shoplist}
    return render(request, 'myadmin/category/add.html', context)


# 执行新增
def insert(request):
    ob = Category()
    ob.name = request.POST['name']
    ob.shop_id = request.POST['shop_id']
    ob.status = 1
    ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    context = {"info": '成功了'}
    return render(request, 'myadmin/info.html', context)


# 删除
def delete(request, cid):
    ob = Category.objects.get(id=cid)
    ob.status = 9
    ob.save()
    context = {'info': '删除成功'}
    return render(request, 'myadmin/info.html', context)


def loadCategory(request, cid):
    clist = Category.objects.filter(status__lt=9, shop_id=cid).values("id", "name")
    # 返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data': list(clist)})


# 加载更新操作
def edit(request, cid):
    ob = Category.objects.get(id=cid)
    slist = Shop.objects.values('id', 'name')
    context = {"category": ob, "shoplist": slist}
    return render(request, 'myadmin/category/edit.html', context)


# 执行更新信息
def update(request, cid):
    ob = Category.objects.get(id=cid)
    ob.shop_id = request.POST['shop_id']
    ob.name = request.POST['name']
    ob.status = request.POST['status']
    ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ob.save()
    context = {'info': '菜品类别更新后成功！'}
    return render(request, 'myadmin/info.html', context)
