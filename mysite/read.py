import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple
import re

def get_file():
	data = xlrd.open_workbook(r'E:\BANG TON KHO th6-2019.xlsx')
	tables = []
	for i in range(0,10):
		tables.append(data.sheet_by_name(f"{i}"))
	return tables

def get_all_type(tables):
	all_type = set()
	for table in tables:
		for row in range(4, table.nrows):
			if table.cell(row, 1).ctype != 0:
				all_type.add(replace_n(table.cell(row, 1).value))
	return all_type

def add_products(tables):
	all_product = []
	for table in tables:
		product_flag = False
		for row in range(4, table.nrows):
			if table.cell(row, 0).ctype != 0:
				product_flag = True
				product_list = []
				product_dict = {}
				remark=''
				if table.cell(row, 0).ctype == 2:
					product_dict['product_id'] =str(int(table.cell(row, 0).value))
				else:
					product_dict['product_id'] = table.cell(row, 0).value
				product_dict['type_of'] = replace_n(table.cell(row, 1).value)
				product_dict['color'] = get_color(table.cell(row, 2).value)
				# if table.cell(row, 1).ctype == 2 or table.cell(row, 2).ctype == 2 :
				# 	print(table,"種類或顏色是數字!",row+1)
				product_dict['price'] = int(get_price(table.cell(row, 3)))
			if table.cell(row, 4).ctype != 0 and table.cell(row, 4).value != 'TONG' and table.cell(row, 4).value != '`':
				if not remark:
					remark = data_process(table.cell(row, 4))
				else:
					remark += ',' + data_process(table.cell(row, 4))
			if table.cell(row, 4).value == 'TONG' or table.cell(row, 5).value == 'NGAY' or table.cell(row, 19).value == 'NGAY' :
				if product_flag:
					for i in product_list:
						i['remarks'] = remark
						all_product.append(i)
					product_flag = False
				continue
			if product_flag:
				product_dict['add_date'] = data_process(table.cell(row, 5))
			for col in range(6, 18):
				if col != 7 and table.cell(row, col).ctype == 2 :
					product_dict['size'] = col+17
					find_flag = False
					for product in product_list:
						if product['size']==product_dict['size']:
							product['quantity'] += int(table.cell(row, col).value)
							find_flag = True
							break
					if find_flag:
						continue
					product_dict['quantity'] = int(table.cell(row, col).value)
					product_list.append(product_dict.copy())
	return all_product
#新的
def add_products(tables):
	all_product = []
	for table in tables:
		product_flag = False
		for row in range(4, table.nrows):
			if table.cell(row, 0).ctype != 0:
				product_flag = True
				product_list = []
				product_dict = {}
				remark=''
				if table.cell(row, 0).ctype == 2:
					product_dict['product_id'] =str(int(table.cell(row, 0).value))
				else:
					product_dict['product_id'] = table.cell(row, 0).value
				product_dict['type_of'] = replace_n(table.cell(row, 1).value)
				product_dict['color'] = get_color(table.cell(row, 2).value)
				product_dict['price'] = int(get_price(table.cell(row, 3)))
			if table.cell(row, 4).ctype != 0 and table.cell(row, 4).value != 'TONG' and table.cell(row, 4).value != '`':
				if not remark:
					remark = data_process(table.cell(row, 4))
				else:
					remark += ',' + data_process(table.cell(row, 4))
			if table.cell(row, 4).value == 'TONG' or table.cell(row, 5).value == 'NGAY' or table.cell(row, 19).value == 'NGAY' :
				if product_flag:
					for i in product_list:
						i['remarks'] = remark
						all_product.append(i)
					product_flag = False
				continue
			if product_flag:
				
			for col in range(6, 18):
				if col != 7 and table.cell(row, col).ctype == 2 :
					product_dict['size'] = col+17
					product_dict['quantity'] = int(table.cell(row, col).value)
					product_list.append(product_dict.copy())
	return all_product

def sold_products(tables):
	sold_product = []
	for table in tables:
		product_flag = False
		for row in range(4, table.nrows):
			if table.cell(row, 0).ctype != 0:
				product_flag = True
				product_dict = {}
				if table.cell(row, 0).ctype == 2:
					product_dict['product_id'] =str(int(table.cell(row, 0).value))
				else:
					product_dict['product_id'] = table.cell(row, 0).value
				product_dict['color'] = get_color(table.cell(row, 2).value)
			if table.cell(row, 4).value == 'TONG' or table.cell(row, 5).value == 'NGAY' or table.cell(row, 19).value == 'NGAY' :
				product_flag = False
				continue
			if product_flag:
				product_dict['sold_date'] = data_process(table.cell(row, 19))
				for col in range(20, 32):
					if col != 21 and table.cell(row, col).ctype == 2 :
						product_dict['size'] = col+3
						product_dict['sell_count'] = int(table.cell(row, col).value)
						sold_product.append(product_dict.copy())
	return sold_product

def get_date(cell):
	if cell.ctype == 0:
		return ""
	elif cell.ctype == 3:
		date = datetime(*xldate_as_tuple(cell.value, 1))
		return = date.strftime('%Y-%d-%m')
	else:
		all_leng = len(cell.value)
		date = cell.value.replace('/', '-')
		if re.match('^\d{4}-\d{1,2}-\d{1,2}', date):
			span = re.match('^\d{4}-\d{1,2}-\d{1,2}', date).span()
			date = date.split('-',2)
			return date[span[0]:span[1]]
		elif re.match('^\d{1,2}-\d{1,2}-\d{4}', date):
			span = re.match('^\d{1,2}-\d{1,2}-\d{4}', date).span()
			date = date[span[0]:span[1]]
			date = date.split('-',2)
			return date[2] + '-' + date[1] + '-' + date[0]
		elif re.match('^\d{1,2}-\d{1,2}', date):
			span = re.match('^\d{1,2}-\d{1,2}', date).span()
			date = date.split('-',2)
			return '0000-' + date[1] + '-' + date[0]
		else :
			print(cell.value)
			
		date_leng = len(add_date)
		if date_leng > all_leng :
			print('bububu', date)

	if cell:
		product_dict['add_date'] = cell

def data_process(cell):
	if cell.ctype == 0 or cell.value == ' ':
		pass
	elif cell.ctype == 3 :
		date = datetime(*xldate_as_tuple(cell.value, 0))
		return date.strftime('%Y/%m/%d')
	elif cell.ctype == 2 :
		if cell.value*100 == int(cell.value*100):
			return str(int(cell.value*100)) + '%'
		return str(cell.value)
	else:
		return replace_n(cell.value)

def replace_n(something):
	if "\n" in something :
		something = something.replace('\n', ' ')
	return something

def get_color(value):
	if " " in value :
		value = value.replace(' ', '')
	return replace_n(value).strip()

def get_price(cell):
	if cell.ctype == 0 or cell.value == ' ':
		return 0
	elif cell.ctype == 2:
		return cell.value
	else:
		return cell.value.replace('K', '')
