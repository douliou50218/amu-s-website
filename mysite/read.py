import xlrd
from datetime import datetime
from xlrd import xldate_as_tuple
import re


def get_file():
    data = xlrd.open_workbook(r'E:\BANG TON KHO th6-2019.xlsx')
    tables = []
    for i in range(0, 10):
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
        for row in range(4, table.nrows):
            if table.cell(row, 0).ctype != 0:
                product_dict = {}
                remark = ''
                if table.cell(row, 0).ctype == 2:
                    product_dict['product_id'] = str(int(table.cell(row, 0).value))
                else:
                    product_dict['product_id'] = table.cell(row, 0).value
                product_dict['type_of'] = replace_n(table.cell(row, 1).value)
                product_dict['color'] = get_color(table.cell(row, 2).value)
                product_dict['price'] = int(get_price(table.cell(row, 3)))

                remark = ''
                i = 0
                while not (table.cell(row + i, 4).value == 'TONG' or table.cell(row + i, 5).value == 'NGAY' or table.cell(row + i, 19).value == 'NGAY'):
                    if not remark:
                        remark = data_process(table.cell(row + i, 4))
                    elif remark and data_process(table.cell(row + i, 4)):
                        remark += ',' + data_process(table.cell(row + i, 4))
                    i += 1

            if table.cell(row, 4).value == 'TONG' or table.cell(row, 5).value == 'NGAY' or table.cell(row, 19).value == 'NGAY':
                continue

            date_text = ''
            if get_date(table.cell(row, 5)):
                product_dict['add_date'] = get_date(table.cell(row, 5))
                if table.cell(row, 5).ctype == 1:
                    date_texts = re.findall('[a-zA-Z]+', table.cell(row, 5).value)
                    print(product_dict['product_id'])
                    for i in date_texts:
                        date_text += i + ' '

            for col in range(6, 18):
                if col != 7 and table.cell(row, col).ctype == 2:
                    product_dict['size'] = col + 17
                    product_dict['quantity'] = int(table.cell(row, col).value)
                    if remark and date_text:
                        product_dict['remarks'] = remark + ',' + date_text.strip()
                    elif remark:
                        product_dict['remarks'] = remark
                    else:
                        product_dict['remarks'] = date_text.strip()
                    all_product.append(product_dict.copy())
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
                    product_dict['product_id'] = str(int(table.cell(row, 0).value))
                else:
                    product_dict['product_id'] = table.cell(row, 0).value
                product_dict['color'] = get_color(table.cell(row, 2).value)

            if table.cell(row, 4).value == 'TONG' or table.cell(row, 5).value == 'NGAY' or table.cell(row, 19).value == 'NGAY':
                product_flag = False
                continue

            if product_flag:
                product_dict['sold_date'] = get_date(table.cell(row, 19))
                if 'cause' in product_dict:
                    del product_dict['cause']
                remark = ''

                if table.cell(row, 19).ctype == 1:
                    date_text = re.findall('[a-zA-Z]+', table.cell(row, 19).value)
                    if date_text:
                        if not remark:
                            remark = ''
                            for i in date_text:
                                remark += i + ' '
                        else:
                            remark += ','
                            for i in date_text:
                                remark += i + ' '

                for col in range(20, 32):
                    if col != 21 and table.cell(row, col).ctype == 2:
                        product_dict['size'] = col + 3
                        product_dict['sell_count'] = int(table.cell(row, col).value)
                        if remark:
                            product_dict['cause'] = remark.strip()
                        sold_product.append(product_dict.copy())

    return sold_product


def get_date(cell):
    if cell.ctype == 0:
        return ""
    elif cell.ctype == 3:
        date = datetime(*xldate_as_tuple(cell.value, 0))
        return date.strftime('%Y-%m-%d')
    else:
        date = re.findall(r'\d{1,5}', cell.value)

        if len(date) == 3:
            if len(date[0]) == 4:
                return date[0] + '-' + date[1] + '-' + date[2]
            else:
                return date[2] + '-' + date[1] + '-' + date[0]
        elif len(date) == 2:
            return '1000-' + date[1] + '-' + date[0]


def data_process(cell):
    if cell.ctype == 0 or cell.value == ' ':
        return ''
    elif cell.ctype == 3:
        date = datetime(*xldate_as_tuple(cell.value, 0))
        return date.strftime('%Y-%m-%d')
    elif cell.ctype == 2:
        if cell.value * 100 == int(cell.value * 100):
            return str(int(cell.value * 100)) + '%'
        return str(cell.value)
    else:
        return replace_n(cell.value)


def replace_n(something):
    if "\n" in something:
        something = something.replace('\n', ' ')
    return something


def get_color(value):
    if " " in value:
        value = value.replace(' ', '')
    return replace_n(value).strip()


def get_price(cell):
    if cell.ctype == 0 or cell.value == ' ':
        return 0
    elif cell.ctype == 2:
        return cell.value
    else:
        return cell.value.replace('K', '')
