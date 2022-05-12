from datetime import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)  # 员工账号
    nickname = models.CharField(max_length=50)  # 昵称
    password_hash = models.CharField(max_length=100)  # 密码
    password_salt = models.CharField(max_length=50)  # 密码混淆值
    status = models.IntegerField(default=1)  # 状态：1正常/2禁用/6管理员/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 更新时间

    def toDict(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname,
                'password_hash': self.password_hash, 'password_salt': self.password_salt, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')
                }

    class Meta:
        db_table = 'user'  # 更改表名


class Shop(models.Model):  # name:名称，cover_pic:封面图片，
    name = models.CharField(max_length=50)  # 店铺的名称
    cover_pic = models.CharField(max_length=250)  # 店铺封面
    banner_pic = models.CharField(max_length=250)  # 店铺logo
    address = models.CharField(max_length=255)  # 店铺地址
    phone = models.CharField(max_length=255)  # 电话
    status = models.IntegerField(default=1)  # 状态：1正常/2暂停/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 更新时间

    def toDict(self):
        shopname = self.name.split("-")
        return {'id': self.id, 'name': self.shopname[0], 'shop': self.shopname[1], 'cover_pic': self.cover_pic,
                'banner_pic': self.banner_pic, 'address': self.address, 'phone': self.phone, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'shop'  # 更改表名


class Category(models.Model):
    shop_id = models.IntegerField()  # 店铺id
    name = models.CharField(max_length=50)  # 分类名称
    status = models.IntegerField()  # 状态：1正常/9删除
    create_at = models.DateTimeField(default=datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.now)  # 更新时间

    class Meta:
        db_table = 'category'  # 更改表名


class Product(models.Model):
    shop_id = models.IntegerField()  # 店铺id
    category_id = models.IntegerField()  # 菜品类别id
    cover_pic = models.CharField(max_length=255)  # 菜品图片
    name = models.CharField(max_length=255)  # 菜品名字
    price = models.CharField(max_length=255)  # 价格
    status = models.IntegerField()  # 状态：1正常   2停售   9下架
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id': self.id, 'shop_id': self.shop_id, 'category_id': self.category_id, 'cover_pic': self.cover_pic,
                'name': self.name, 'price': self.price, 'status': self.status,
                'create_at': self.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'product'
