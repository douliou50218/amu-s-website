from django.db import models
import datetime


# Create your models here.
class Size(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=7)

    def __str__(self):
        return str(self.number)


class TypeOf(models.Model):
    type_of = models.CharField(primary_key=True, max_length=50)


class Clerk(models.Model):
    clerk_name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.clerk_name


class Customer(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.phone_number


class All_Product(models.Model):
    product_id = models.CharField(max_length=50)
    type_of = models.ForeignKey(
        TypeOf,
        models.PROTECT,
        null=True,
    )
    color = models.CharField(
        max_length=50,
        null=True,
    )
    add_date = models.DateField(
        default=datetime.date.today().strftime("%Y-%m-%d"),
        null=True,
    )
    size = models.ForeignKey(
        Size,
        models.PROTECT,
    )
    price = models.IntegerField(default=0)
    remarks = models.CharField(
        max_length=1000,
        blank=True,
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_id


class Sales_Record(models.Model):
    # 多个foreignkey指向同一个主表，related_name必须设置。
    product = models.ForeignKey(
        All_Product,
        models.PROTECT,
    )
    sell_count = models.IntegerField()
    customer = models.ForeignKey(
        Customer,
        models.PROTECT,
        blank=True,
        null=True,
    )
    sell_price = models.IntegerField(default=-9999)
    sale_date = models.DateField(
        default=datetime.date.today().strftime("%Y-%m-%d"),
        null=True,
    )
    clerk = models.ForeignKey(
        Clerk,
        models.PROTECT,
        null=True,
    )
    remark = models.CharField(
        max_length=1000,
        blank=True,
    )


class TodayRecord(models.Model):
    product = models.ForeignKey(
        All_Product,
        models.PROTECT,
    )
    sell_count = models.IntegerField()
    base_price = models.IntegerField()
    sell_price = models.IntegerField()
    customer = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    clerk = models.ForeignKey(
        Clerk,
        models.PROTECT,
    )
    remark = models.CharField(
        max_length=1000,
        blank=True,
    )
