for i in all_product[:5]:
    print(i)

for i in sold_product[:5]:
    print(i)

for i in all_product:
	if i['product_id'] == '2016':
		print(i)

for i in sold_product:
	if i['product_id'] == '173':
		print(i)

#-----------------------------------------------------------------
from pos.models import *
import read

tables=read.get_file()
all_type = read.get_all_type(tables)

for i in all_type:
	TypeOf.objects.get_or_create(type_of=i)

all_product = read.add_products(tables)

#這裡重寫
for i in all_product:
	if i['type_of'] !='' :
		All_Product.objects.create(product_id=i['product_id'],type_of=TypeOf.objects.get(type_of=i['type_of']),color=i['color'],add_date=i['add_date'],size=i['size'],price=i['price'],remarks=i['remarks'],quantity=i['quantity'])
	else:
		All_Product.objects.create(product_id=i['product_id'],color=i['color'],add_date=i['add_date'],size=i['size'],price=i['price'],remarks=i['remarks'],quantity=i['quantity'])


sold_product=read.sold_products(tables)

for sold in sold_product:
	try:
		sold_pdt = All_Product.objects.get(product_id=sold['product_id'], color=sold['color'], size=sold['size'])
		sold_pdt.quantity -= sold['sell_count']
		sold_pdt.save()
	except All_Product.DoesNotExist:
		product = All_Product.objects.filter(product_id=sold['product_id'], color=sold['color'])
		All_Product.objects.create(product_id=sold['product_id'],color=sold['color'],add_date='',size=sold['size'],price=product[0].price,remarks=product[0].remarks,quantity=0-sold['sell_count'])
		sold_pdt = All_Product.objects.get(product_id=sold['product_id'], color=sold['color'], size=sold['size'])
	sale_rd = Sales_Record(product=sold_pdt)
	sale_rd.sell_count = sold['sell_count']
	sale_rd.sell_price = -1487
	sale_rd.sale_date = sold['sold_date']
	sale_rd.save()


Sales_Record.objects.all().delete()
All_Product.objects.all().delete()

#檢查總數
aaa=All_Product.objects.all()
num=0
for i in aaa:
    num+=i.quantity
aaa=Sales_Record.objects.all()
num=0
for i in aaa:
    num+=i.sell_count


num
#-----------------------------------------------------------------#
#開減
for sold in sold_product:
	for i in all_product:
		if sold['product_id'] != i['product_id']:
			continue
		elif sold['color'] != i['color']:
			continue
		elif sold['size'] != i['size']:
			continue
		else:
			i['quantity'] -= sold['sell_count']
			break
	else:
		product_dict={}
		for i in all_product:
			if sold['product_id'] == i['product_id'] and sold['color'] == i['color']:
				for key in i:
					product_dict[key]=i[key]
				product_dict['add_date']=''
				product_dict['size']=sold['size']
				product_dict['quantity']=0-sold['sell_count']
				print(product_dict)
				break
		all_product.append(product_dict)
#減完後的table商品數
i=0
num=0
for n in range(0,10):
	table_num=0
	flag=False
	while i != len(all_product) :
		for str_num in range(0,len(all_product[i]['product_id'])):
			if all_product[i]['product_id'][str_num] == str(n) :
				table_num += all_product[i]['quantity']
				i += 1
				break
			elif all_product[i]['product_id'][str_num] == str(n+1) :
				flag=True
				break
		if flag :
			break
	print(table_num)
	num+=table_num

num=0
for i in all_product:
	num += i['quantity']
print(num)

num=0
for i in sold_product:
	num += i['sell_count']
print(num)

for i in product_num:
	aaa=0
	for j in all_product:
		if j['product_id'] == i['product_id'] and j['color'] == i['color']:
			aaa+=j['quantity']
	if i['num'] != aaa:
		print(i,aaa)
