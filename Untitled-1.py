for i in all_product[:5]:
    print(i)

for i in sold_product[:5]:
    print(i)

for i in all_product:
	if i['product_id'] == '823':
		print(i)

for i in sold_product:
	if i['product_id'] == '9108':
		print(i)

#-----------------------------------------------------------------
from pos.models import *
import read

aaa = (
    (23, 'F'),
    (25, '25 XS'),
    (26, '26 S'),
    (27, '27 M'),
    (28, '28 L'),
    (29, '39 XL'),
    (30, '30 2XL'),
    (31, '31 3XL'),
    (32, '32 4XL'),
    (33, '5XL'),
    (34, '6XL'),
)
for i in aaa:
	size = Size(number=i[0], name=i[1])
	size.save()



tables=read.get_file()
all_type = read.get_all_type(tables)

for i in all_type:
	TypeOf.objects.get_or_create(type_of=i)

all_product = read.add_products(tables)

for i in all_product:
	pd = All_Product()
	pd.product_id = i['product_id']
	pd.color = i['color']
	if 'add_date' in i:
		pd.add_date = i['add_date']
	pd.size = Size.objects.get(number=i['size'])
	pd.price = i['price']
	pd.remarks = i['remarks']
	pd.quantity = i['quantity']
	if i['type_of'] != '':
		pd.type_of = TypeOf.objects.get(type_of=i['type_of'])
	pd.save()
	#All_Product.objects.create(product_id=i['product_id'],color=i['color'],add_date=i['add_date'],size=i['size'],price=i['price'],remarks=i['remarks'],quantity=i['quantity'])


sold_product=read.sold_products(tables)

for sold in sold_product:
	#_gt 大於 __gte 大於等於 __lt 小於 __lte 小於等於
	sold_pdts = All_Product.objects.filter(product_id=sold['product_id'], color=sold['color'], size=Size.objects.get(number=sold['size']))
	if sold_pdts:
		sold_pdt = sold_pdts[0]
		sold_pdt.quantity -= sold['sell_count']
		sold_pdt.save()
	else:
		try:
			product = All_Product.objects.filter(product_id=sold['product_id'], color=sold['color'])
			pd = All_Product()
			pd.product_id = sold['product_id']
			if product[0].type_of:
				pd.type_of = product[0].type_of
			pd.color = sold['color']
			pd.size = Size.objects.get(number=sold['size'])
			pd.price = product[0].price
			pd.remarks = product[0].remarks
			pd.quantity = 0-sold['sell_count']
			pd.save()
			#All_Product.objects.create( product_id=sold['product_id'],color=sold['color'],size=sold['size'],price=product[0].price,remarks=product[0].remarks,quantity=0-sold['sell_count'])
			sold_pdt = All_Product.objects.get(product_id=sold['product_id'], color=sold['color'], size=sold['size'])
		except Exception as e:
			print(e,sold)
	sale_rd = Sales_Record(product=sold_pdt)
	sale_rd.sell_count = sold['sell_count']
	sale_rd.sell_price = -1000
	if sold['sold_date']:
		sale_rd.sale_date = sold['sold_date']
	if 'cause' in sold:
		sale_rd.remark = sold['cause']
	else:
		sale_rd.remark = ""
	sale_rd.save()


#清除資料
Sales_Record.objects.all().delete()
All_Product.objects.all().delete()

#檢查總數
aaa=All_Product.objects.all()
num=0
for i in aaa:
    num+=i.quantity

num

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
