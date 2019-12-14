from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from .models import All_Product, Clerk, Customer, Sales_Record, TodayRecord, TypeOf
from django.http import HttpResponse
from django.contrib import auth  # 別忘了import auth
from django.contrib.auth.models import User  #記得要先導入套件


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    account = User.objects.all()
    print(account)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'login.html', {'account': account, })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')


def index(request):
    all_products = All_Product.objects.exclude(quantity=0)
    all_count = 0
    outside = []
    for product in all_products:
        aaa = {'product_id': product.product_id, 'color': product.color}
        for i in outside:
            if aaa['product_id'] == i['product_id'] and aaa['color'] == i['color']:
                break
        else:
            outside.append(aaa)

        all_count += product.quantity

    clerk = Clerk.objects.all()
    clerk_sales = []
    sale_dict = {}
    for i in clerk:
        # 這裡要分月份
        sales = Sales_Record.objects.filter(clerk=i)
        sale_dict['clerk'] = i.clerk_name
        sale_dict['sales_num'] = len(sales)
        clerk_sales.append(sale_dict.copy)

    context = {
        'outside': outside,
        'inside': all_count - len(outside),
        'all_count': all_count,
        'clerk_sales': clerk_sales,
    }
    return render(request, 'index.html', context)


def storage(request):
    with connection.cursor() as c:
        c.execute('''SELECT product_id, type_of_id, color, size, quantity, add_date, price, remarks 
            FROM pos_all_product 
            WHERE NOT quantity = 0''')
        stock_products = c.fetchall()

    context = {
        'stock_products': stock_products,
    }
    return render(request, 'storage.html', context)


def already_sold(request):
    with connection.cursor() as c:
        c.execute('''SELECT
                pap.product_id, pap.type_of_id, pap.color, pap.size, psr.sale_date, psr.clerk_id, pap.price, psr.sell_price, psr.sell_count, psr.customer_id, pap.remarks
            FROM pos_Sales_Record as psr
            JOIN pos_All_Product as pap on psr.product_id = pap.id''')
        sold_products = c.fetchall()

    context = {
        'sold_products': sold_products,
    }
    return render(request, 'already sold.html', context)


def sold_today(request):
    if 'type' in request.POST:
        if request.POST.get('type') == 'product':

            product = request.POST.get('product')
            search_product = All_Product.objects.filter(product_id=product).exclude(quantity='0')

            color = []
            if search_product:
                for product in search_product:
                    if product.color not in color:
                        color.append(product.color)

            response = JsonResponse({"repeat": color})

        elif request.POST.get('type') == 'color':

            product = request.POST.get('product')
            color = request.POST.get('color')
            search_product = All_Product.objects.filter(product_id=product, color=color).exclude(quantity='0')

            size = []

            if search_product:
                for product in search_product:
                    if product.size not in size:
                        size.append(product.size)

            response = JsonResponse({"repeat": size})

        elif request.POST.get('type') == 'count':

            product = request.POST.get('product')
            color = request.POST.get('color')
            size = request.POST.get('size')
            search_count = All_Product.objects.get(product_id=product, color=color, size=size)
            response = JsonResponse({"repeat": search_count.quantity})

        return response

    elif 'number' in request.POST:
        print(request.POST.get('number'))
        record = TodayRecord.objects.all()
        d = record[int(request.POST.get('number')) - 1]
        d.delete()

    elif request.POST.get('submit'):
        p = TodayRecord()
        p.product = All_Product.objects.get(product_id=request.POST.get('product'), color=request.POST.get('color'),
                                            size=request.POST.get('size'))
        p.sell_count = request.POST.get('count')
        p.base_price = p.product.price
        p.sell_price = request.POST.get('price')
        p.clerk = Clerk.objects.get(clerk_name=request.POST.get('clerk'))
        p.customer = request.POST.get('phone')
        p.save()

    customer = Customer.objects.all()
    stock_products = All_Product.objects.exclude(quantity=0)
    all_pdtid = []
    for i in stock_products:
        if i.product_id not in all_pdtid:
            all_pdtid.append(i.product_id)
    clerk = Clerk.objects.all()

    # 退貨時商品搜尋
    with connection.cursor() as c:
        c.execute('''SELECT pap.product_id, pap.color, pap.size, psr.sale_date, psr.sell_price, psr.sell_count, psr.customer_id
                FROM pos_Sales_Record as psr
                JOIN pos_All_Product as pap on psr.product_id = pap.id''')
        sold_products = c.fetchall()
    sold_pdtid = []
    for i in sold_products:
        if i[0] not in sold_pdtid:
            sold_pdtid.append(i[0])
    # 結算
    record = TodayRecord.objects.all()
    rcd_money = 0
    rcd_length = 0
    for i in record:
        rcd_money += i.sell_price
        rcd_length += i.sell_count

    context = {
        'all_pdtid': all_pdtid,
        'customer': customer,
        'clerk': clerk,
        'sold_pdtid': sold_pdtid,
        'record': zip(range(1, len(record) + 1), record),
        'rcd_money': rcd_money,
        'rcd_length': rcd_length,
    }

    return render(request, 'sold today.html', context)


def add_new(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        type_of = TypeOf.objects.all()

        context = {
            'type_of': type_of,
        }

    if 'product_submit' in request.POST:
        print("aaaaa")
        # product = All_Product()
        # product.product_id = request.POST['type_of']
        # product.save()
    elif 'clerk_submit' in request.POST:
        Clerk.objects.get_or_create(clerk_name=request.POST['clerk'])
    elif 'type_submit' in request.POST:
        TypeOf.objects.get_or_create(type_of=request.POST['type_of'])


    return render(request, 'add new.html', context)


@login_required
def add_type(request):
    if request.method == "POST":
        TypeOf.objects.get_or_create(type_of=request.POST['type_of'])
    return render(request, 'add_type.html')
