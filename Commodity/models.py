from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User


# Create your models here.

class Commodity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, max_length=100, editable=False,
                          db_column='商品编号')
    name = models.CharField(max_length=60, db_column='商品名称')
    image = models.ImageField(upload_to='Commodity', default='Commodity/defaultimag.png',blank=True, null=True, db_column='商品图片')
    price = models.DecimalField(max_digits=20, decimal_places=2, db_column='商品价格')
    date = models.DateTimeField(auto_now_add=True, db_column='上传日期')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='所属人')
    public = models.BooleanField(default=True, db_column='公开标志')
    selltag = models.BooleanField(default=False, db_column='售出标志')
    details = models.TextField(max_length=200, blank=False, null=True, default="", db_column='详细信息')
    count = models.IntegerField(default=0, db_column='加购次数')

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    commodity = models.ForeignKey('Commodity', unique=False, on_delete=models.CASCADE, db_column='商品编号')
    adduser = models.ForeignKey(User, unique=False, default="", on_delete=models.CASCADE, db_column='加购人')
    date = models.DateTimeField(auto_now_add=True, db_column='加购日期')


class Order(models.Model):
    orderid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, max_length=100, editable=False,
                               db_column='订单编号')
    commodity_id = models.ForeignKey('Commodity', unique=False, on_delete=models.CASCADE, db_column='商品编号')
    date = models.DateTimeField(auto_now_add=True, db_column='创建日期')
    seller = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, db_column='卖方')
    purchaser = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='buyer',db_column='‘买方')
    remark = models.TextField(max_length=100, blank=True, null=True, default="", db_column='备注')
    donetag = models.BooleanField(default=False, db_column='完成标志')
    senttag = models.BooleanField(default=False, db_column='发货标志')
    receipttag = models.BooleanField(default=False, db_column='收货标志')
    backtag = models.BooleanField(default=False, db_column='退货标志')
    preoder = models.ForeignKey('Order', unique=False, blank=True, null=True, on_delete=models.CASCADE,
                                db_column='前置单号')
    tracking_number = models.CharField(max_length=20, blank=False, null=True, db_column='快递单号')

    def __int__(self):
        return self.orderid


class Message(models.Model):
    name = models.ForeignKey(Commodity, unique=False, blank=False, on_delete=models.CASCADE, db_column='商品名称')
    speaker = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, db_column='留言者')
    content = models.TextField(max_length=200, blank=False, default="", db_column='留言内容')
    date = models.DateTimeField(auto_now_add=True, db_column='发言日期')

    def __str__(self):
        return f"{self.content[0:30]}"


class Search_History(models.Model):
    id = models.ForeignKey(User, unique=True, blank=True, on_delete=models.CASCADE, primary_key=True)
    str = models.TextField(max_length=10000, blank=False, default="", db_column='最近一次搜索记录')

    def __str__(self):
        return f"{self.str[0:30]}"
