from django.contrib import admin

# Register your models here.
from .models import TypeOf, Clerk, Customer, All_Product, Sales_Record, TodayRecord

admin.site.register(TypeOf)
admin.site.register(Clerk)
admin.site.register(Customer)
admin.site.register(All_Product)
admin.site.register(Sales_Record)
admin.site.register(TodayRecord)
