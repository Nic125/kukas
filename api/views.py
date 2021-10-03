import os
import time

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import *
from .serializers import *
from django.core.files.storage import default_storage

@csrf_exempt
def category(request, id=0):
    if request.method == 'GET':
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        return JsonResponse(category_serializer.data, safe=False)
    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Categoría creada con éxito", safe=False)
        return JsonResponse(f"Error al crear la categoría", safe=False)
    elif request.method == 'PUT':
        category_data = JSONParser().parse(request)
        category = Category.objects.get(id=category_data['id'])
        category_serializer = CategorySerializer(category, data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Categoría actualizada con éxito", safe=False)
        return JsonResponse("Error al actualizar la Categoría", safe=False)
    elif request.method == "DELETE":
        category = Category.objects.get(id=id)
        category.delete()
        return JsonResponse("Categoría eliminada con éxito", safe=False)

@csrf_exempt
def subcategory(request, id=0):
    if request.method == 'GET':
        subcategory_data = request.GET['category_id']
        subcategory = Subcategory.objects.filter(category_id=subcategory_data)
        subcategory_serializer = SubcategorySerializerGet(subcategory, many=True)
        return JsonResponse(subcategory_serializer.data, safe=False)
    elif request.method == 'POST':
        subcategory_data = JSONParser().parse(request)
        subcategory_serializer = SubcategorySerializer(data=subcategory_data)
        if subcategory_serializer.is_valid():
            subcategory_serializer.save()
            return JsonResponse("Subcategoría creada con éxito", safe=False)
        return JsonResponse("Error al crear la subcategoría", safe=False)
    elif request.method == 'PUT':
        subcategory_data = JSONParser().parse(request)
        subcategory = Subcategory.objects.get(id=subcategory_data['id'])
        subcategory_serializer = SubcategorySerializer(subcategory, data=subcategory_data)
        if subcategory_serializer.is_valid():
            subcategory_serializer.save()
            return JsonResponse("Subcategoría actualizada con éxito", safe=False)
        return JsonResponse("Error al actualizar la subcategoría", safe=False)
    elif request.method == "DELETE":
        subcategory = Subcategory.objects.get(id=id)
        subcategory.delete()
        return JsonResponse("Subcategoría eliminada con éxito", safe=False)

@csrf_exempt
def expenses(request, id=0):
    if request.method == 'GET':
        expenses = Expenses.objects.all()
        expenses_serializer = ExpensesSerializer(expenses, many=True)
        return JsonResponse(expenses_serializer.data, safe=False)
    elif request.method == 'POST':
        expenses_data = JSONParser().parse(request)
        expenses_serializer = ExpensesSerializer(data=expenses_data)
        if expenses_serializer.is_valid():
            expenses_serializer.save()
            return JsonResponse("El gasto se registro con éxito", safe=False)
        return JsonResponse("Error al registrar el gasto con éxito", safe=False)
    elif request.method == 'PUT':
        expenses_data = JSONParser().parse(request)
        expenses = Expenses.objects.get(id=expenses_data['id'])
        expenses_serializer = ExpensesSerializer(expenses, data=expenses_data)
        if expenses_serializer.is_valid():
            expenses_serializer.save()
            return JsonResponse("El gasto fue actualizado con éxito", safe=False)
        return JsonResponse("Error al actualizar el gasto", safe=False)
    elif request.method == "DELETE":
        expenses = Expenses.objects.get(id=id)
        expenses.delete()
        return JsonResponse("El gasto se eliminó con éxito", safe=False)

@csrf_exempt
def product(request, id=0):
    if request.method == 'GET':
        product_data = request.GET['subcategory_id']
        product = Product.objects.filter(subcategory_id=product_data)
        product_serializer = ProductSerializerGet(product, many=True)
        return JsonResponse(product_serializer.data, safe=False)
    elif request.method == 'POST':
        product_data = JSONParser().parse(request)
        subcategory_id = Subcategory.objects.get(id=product_data['subcategory_id'])
        product = Product.objects.create(
            name=product_data['name'],
            code=product_data['code'],
            description=product_data['description'],
            subcategory_id=subcategory_id,
            cost=product_data['cost'],
            profit=product_data['profit'],
            photo_file_name=product_data['photo_file_name'],
            photo_file_name2 = product_data['photo_file_name2'],
            photo_file_name3 = product_data['photo_file_name3']
        )

        product.save()

        for expense in product_data['expenses']:
            expense_obj = Expenses.objects.get(id=expense)
            product.expenses.add(expense_obj)

        return JsonResponse("Producto creado con éxito", safe=False)

    elif request.method == 'PUT':
        product_data = JSONParser().parse(request)

        if product_data['update'] == "highlight":
            items = product_data['items']
            for item in items:
                product_edit = Product.objects.get(id=item)
                if product_edit.highlight == "0":
                    product_edit.highlight = "1"
                    product_edit.save()
                else:
                    product_edit.highlight = "0"
                    product_edit.save()

        elif product_data['update'] == "discount":
            items = product_data['items']
            for item in items:
                product_edit = Product.objects.get(id=item)
                product_edit.on_sale = product_data['amount']
                product_edit.save()

        else:
            product_edit = Product.objects.get(id=product_data['id'])
            subcategory_id = Subcategory.objects.get(id=product_data['subcategory_id'])
            product_edit.name = product_data['name']
            product_edit.code = product_data['code']
            product_edit.description = product_data['description']
            product_edit.subcategory_id = subcategory_id
            product_edit.cost = product_data['cost']
            product_edit.profit = product_data['profit']
            product_edit.photo_file_name = product_data['photo_file_name']
            product_edit.photo_file_name2 = product_data['photo_file_name2']
            product_edit.photo_file_name3 = product_data['photo_file_name3']
            product_edit.expenses.set([])

            product_edit.save()

            for expense in product_data['expenses']:
                expense_obj = Expenses.objects.get(id=expense)
                product_edit.expenses.add(expense_obj)


        return JsonResponse("Producto actualizado con éxito", safe=False)

    elif request.method == "DELETE":
        product = Product.objects.get(id=id)
        if os.path.isfile(product.photo_file_name):
            os.remove(product.photo_file_name)
        if os.path.isfile(product.photo_file_name2):
            os.remove(product.photo_file_name2)
        if os.path.isfile(product.photo_file_name3):
            os.remove(product.photo_file_name3)
        product.delete()
        return JsonResponse("El producto se a eliminado con éxito", safe=False)

@csrf_exempt
def stock(request, id=0):
    if request.method == 'GET':
        if request.GET['product_id']:
            stock_data = request.GET['product_id']
            stock = Stock.objects.filter(product_id=stock_data)
            stock_serializer = StockSerializerGet(stock, many=True)
            return JsonResponse(stock_serializer.data, safe=False)
    elif request.method == 'POST':
        stock_data = JSONParser().parse(request)
        stock_serializer = StockSerializer(data=stock_data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse("Stock creado con éxito", safe=False)
        return JsonResponse(f"Error al crear stock", safe=False)
    elif request.method == 'PUT':
        stock_data = JSONParser().parse(request)
        stock = Stock.objects.get(id=stock_data['id'])
        stock_serializer = StockSerializer(stock, data=stock_data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse("Stock actualizado con éxito", safe=False)
        return JsonResponse("Error al actualizar el stock", safe=False)
    elif request.method == "DELETE":
        stock = Stock.objects.get(id=id)
        stock.delete()
        return JsonResponse("stock eliminado con éxito", safe=False)


@csrf_exempt
def SaveFile(request):
    file = request.FILES['uploadedFile']
    file_name = default_storage.save(file.name, file)

    return JsonResponse(file_name, safe=False)


@csrf_exempt
def get_products(request):
    selected_category = request.GET['category_id']
    products_list = []
    products = Product.objects.filter(subcategory_id__category_id=selected_category)

    for product in products:
        add = 0
        percentage = 0
        iva = 0

        expenses_list = product.expenses.all()

        for expense in expenses_list:
            ex = Expenses.objects.get(name=expense)
            if ex.type_value == "$":
                add += int(ex.value)
            elif ex.name == "IVA":
                iva += int(ex.value)
            elif ex.type_value == "%" and ex.name != "IVA":
                percentage += int(ex.value)

        final_price = int(product.cost) + ((int(product.profit) * int(product.cost)) / 100)
        final_price_per = final_price + ((percentage * final_price) / 100)
        final_price_add = final_price_per + add
        final_price_iva = final_price_add + ((iva * final_price_add) / 100)

        sale = 0

        if product.on_sale != "0":
            on_sale_price = final_price_iva - ((int(product.on_sale) * final_price_iva) / 100)
            sale = on_sale_price

        stock = Stock.objects.filter(product_id=product.id)

        stock_amount = 0

        for item in stock:
            stock_amount += int(item.amount)

        products_list.append((
            {
                'id': product.id,
                'name': product.name,
                'subcategory': product.subcategory_id.name,
                'category': product.subcategory_id.category_id.name,
                'description': product.description,
                'photo_file_name': product.photo_file_name,
                'photo_file_name2': product.photo_file_name2,
                'photo_file_name3': product.photo_file_name3,
                'highlight': product.highlight,
                'on_sale': product.on_sale,
                'price': round(final_price_iva),
                'sale_price': round(sale),
                'stock': stock_amount
             }
        ))

    return JsonResponse({'products': products_list})


@csrf_exempt
def get_products_search(request):
    search_name = request.GET['name']
    products_list = []
    products = Product.objects.filter(name__icontains=search_name)

    for product in products:
        add = 0
        percentage = 0
        iva = 0

        expenses_list = product.expenses.all()

        for expense in expenses_list:
            ex = Expenses.objects.get(name=expense)
            if ex.type_value == "$":
                add += int(ex.value)
            elif ex.name == "IVA":
                iva += int(ex.value)
            elif ex.type_value == "%" and ex.name != "IVA":
                percentage += int(ex.value)

        final_price = int(product.cost) + ((int(product.profit) * int(product.cost)) / 100)
        final_price_per = final_price + ((percentage * final_price) / 100)
        final_price_add = final_price_per + add
        final_price_iva = final_price_add + ((iva * final_price_add) / 100)

        sale = 0

        if product.on_sale != "0":
            on_sale_price = final_price_iva - ((int(product.on_sale) * final_price_iva) / 100)
            sale = on_sale_price

        stock = Stock.objects.filter(product_id=product.id)

        stock_amount = 0

        for item in stock:
            stock_amount += int(item.amount)

        products_list.append((
            {
                'id': product.id,
                'name': product.name,
                'subcategory': product.subcategory_id.name,
                'category': product.subcategory_id.category_id.name,
                'description': product.description,
                'photo_file_name': product.photo_file_name,
                'photo_file_name2': product.photo_file_name2,
                'photo_file_name3': product.photo_file_name3,
                'highlight': product.highlight,
                'on_sale': product.on_sale,
                'price': round(final_price_iva),
                'sale_price': round(sale),
                'stock': stock_amount
             }
        ))

    return JsonResponse({'products': products_list})


def get_all_products_final_admin(request):
    time.sleep(.5)
    products_list = []
    products = Product.objects.all()

    for product in products:
        add = 0
        percentage = 0
        iva = 0

        expenses_list = product.expenses.all()

        for expense in expenses_list:
            ex = Expenses.objects.get(name=expense)
            if ex.type_value == "$":
                add += int(ex.value)
            elif ex.name == "IVA":
                iva += int(ex.value)
            elif ex.type_value == "%" and ex.name != "IVA":
                percentage += int(ex.value)

        final_price = int(product.cost) + ((int(product.profit) * int(product.cost)) / 100)
        final_price_per = final_price + ((percentage * final_price) / 100)
        final_price_add = final_price_per + add
        final_price_iva = final_price_add + ((iva * final_price_add) / 100)

        sale = 0

        if product.on_sale != "0":
            on_sale_price = final_price_iva - ((int(product.on_sale) * final_price_iva) / 100)
            sale = on_sale_price

        stock = Stock.objects.filter(product_id=product.id)

        stock_amount = 0

        for item in stock:
            stock_amount += int(item.amount)

        products_list.append((
            {
                'id': product.id,
                'name': product.name,
                'subcategory': product.subcategory_id.name,
                'category': product.subcategory_id.category_id.name,
                'photo_file_name': product.photo_file_name,
                'highlight': product.highlight,
                'on_sale': product.on_sale,
                'price': round(final_price_iva),
                'sale_price': round(sale),
                'stock': stock_amount
             }
        ))

    return JsonResponse({'products': products_list})


@csrf_exempt
def get_all_highlight(request):
    time.sleep(.2)
    products_list = []
    products = Product.objects.filter(highlight="1")

    for product in products:
        add = 0
        percentage = 0
        iva = 0

        expenses_list = product.expenses.all()

        for expense in expenses_list:
            ex = Expenses.objects.get(name=expense)
            if ex.type_value == "$":
                add += int(ex.value)
            elif ex.name == "IVA":
                iva += int(ex.value)
            elif ex.type_value == "%" and ex.name != "IVA":
                percentage += int(ex.value)

        final_price = int(product.cost) + ((int(product.profit) * int(product.cost)) / 100)
        final_price_per = final_price + ((percentage * final_price) / 100)
        final_price_add = final_price_per + add
        final_price_iva = final_price_add + ((iva * final_price_add) / 100)

        sale = 0

        if product.on_sale != "0":
            on_sale_price = final_price_iva - ((int(product.on_sale) * final_price_iva) / 100)
            sale = on_sale_price

        stock = Stock.objects.filter(product_id=product.id)

        stock_amount = 0

        for item in stock:
            stock_amount += int(item.amount)

        products_list.append((
            {
                'id': product.id,
                'name': product.name,
                'subcategory': product.subcategory_id.name,
                'category': product.subcategory_id.category_id.name,
                'description': product.description,
                'photo_file_name': product.photo_file_name,
                'photo_file_name2': product.photo_file_name2,
                'photo_file_name3': product.photo_file_name3,
                'highlight': product.highlight,
                'on_sale': product.on_sale,
                'price': round(final_price_iva),
                'sale_price': round(sale),
                'stock': stock_amount
            }
        ))

    return JsonResponse({'products': products_list})


@csrf_exempt
def get_all_products(request):
    products = Product.objects.all()
    product_serializer = ProductSerializerGet(products, many=True)
    return JsonResponse(product_serializer.data, safe=False)


@csrf_exempt
def get_all_stock(request, id=0):
    if request.method == 'GET':
        stock = Stock.objects.all()
        stock_serializer = StockSerializer(stock, many=True)
        return JsonResponse(stock_serializer.data, safe=False)


def pending_sell(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = JSONParser().parse(request)
            user = User.objects.get(id=data['client_id'])

            new_sell = PendingSell(
                total=data['total'],
                client_id=user
            )
            new_sell.save()

            sell_id = PendingSell.objects.get(id=new_sell.id)

            for item in data['order']:
                item_details = item['item']
                product = Product.objects.get(id=int(item_details['id']))
                stock = Stock.objects.get(product_id=int(item_details['id']), name=item['size'])
                amount = int(stock.amount)
                stock.amount = amount - int(item['amount'])
                stock.save()

                sell_details = SellDetails(
                    sell=sell_id,
                    product_id=product,
                    size=item['size'],
                    amount=item['amount'],
                    price=item_details['price']
                )
                sell_details.save()

        return JsonResponse({'response': 'ok'})


@csrf_exempt
def cancel_pending_sell(request, id=0):
    if request.method == "DELETE":
        details = SellDetails.objects.filter(sell_id=id)
        for item in details:
            restore_stock = Stock.objects.get(product_id=item.product_id, name=item.size)
            restore_stock.amount = int(restore_stock.amount) + int(item.amount)
            restore_stock.save()
            item.delete()
        sell = PendingSell.objects.get(id=id)
        sell.delete()
        return JsonResponse("La venta se eliminó con éxito", safe=False)



def all_sells_in_process(request):
    sell_list = []
    pending = PendingSell.objects.all()

    for sell in pending:
        details_list = []
        details = SellDetails.objects.filter(sell=sell.id)
        for item in details:
            details_list.append({
                'product': item.product_id.name,
                'product_id': item.product_id.id,
                'product_code': item.product_id.code,
                'size': item.size,
                'amount': item.amount,
                'price': item.price
            })
        sell_list.append({
            'id': sell.id,
            'date': sell.date_posted,
            'client': sell.client_id.email,
            'client_id': sell.client_id.id,
            'total': sell.total,
            'details': details_list
        })
    return JsonResponse({'sell_list': sell_list})


def client_data(request, id=0):
    if request.method == 'GET':
        user_id = request.GET['user_id']
        client_data = ClientData.objects.filter(user_id=user_id)
        client_serializer = ClientDataSerializer(client_data, many=True)
        return JsonResponse(client_serializer.data, safe=False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        client_serializer = ClientDataSerializer(data=user_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return JsonResponse("Datos cargados con éxito", safe=False)
        return JsonResponse("Error al cargar los datos", safe=False)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        client_data = ClientData.objects.get(id=user_data['id'])
        client_serializer = ClientDataSerializer(client_data, data=user_data)
        if client_serializer.is_valid():
            client_serializer.save()
            return JsonResponse("Datos actualizados con éxito", safe=False)
        return JsonResponse("Error al actualizar los datos", safe=False)
    elif request.method == "DELETE":
        user_data = ClientData.objects.get(id=id)
        user_data.delete()
        return JsonResponse("Datos eliminados con éxito", safe=False)


def all_client_data(request):
    if request.method == 'GET':
        users = User.objects.filter(is_staff=False, is_active=True)

        user_list = []

        for user in users:
            data = ClientData.objects.get(user_id=user.id)
            user_list.append({
                'user_id': user.id,
                'data_id': data.id,
                'username': user.username,
                'email': user.email,
                'first_name': data.first_name,
                'last_name': data.last_name,
                'address': data.address,
                'province': data.province,
                'city': data.city,
                'neighborhood': data.neighborhood,
                'cp': data.cp,
                'phone': data.phone

            })

        return JsonResponse({'clients_data': user_list})



def sell(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pending_sell = PendingSell.objects.get(id=data['id'])
        sale_details = SellDetails.objects.filter(sell_id=pending_sell.id)

        sale = Sell(
            shipping=data['guide'],
            total=pending_sell.total,
            client=pending_sell.client_id,
        )

        sale.save()

        for item in sale_details:
            close_sale_details = CloseSellDetails(
                sell=sale,
                product_name=item.product_id.name,
                size=item.size,
                amount=item.amount,
                price=item.price,
            )
            close_sale_details.save()
            item.delete()

        pending_sell.delete()
        return JsonResponse("Error al registrar la venta con éxito", safe=False)


def all_sells_close(request):
    sell_list = []
    sells = Sell.objects.all()

    for sell in sells:
        details_list = []
        details = CloseSellDetails.objects.filter(sell=sell.id)
        for item in details:
            details_list.append({
                'product': item.product_name,
                'size': item.size,
                'amount': item.amount,
                'price': item.price
            })
        sell_list.append({
            'id': sell.id,
            'date': sell.date_posted,
            'shipping': sell.shipping,
            'client': sell.client.email,
            'client_id': sell.client.id,
            'total': sell.total,
            'details': details_list
        })

    return JsonResponse({'sell_list': sell_list})



def buys_users(request):
    user_id = request.GET['user_id']
    sell_list = []
    pending = PendingSell.objects.filter(client_id=user_id)
    sells = Sell.objects.filter(client=user_id)

    for sell in pending:
        details_list = []
        details = SellDetails.objects.filter(sell=sell.id)
        for item in details:
            details_list.append({
                'product': item.product_id.name,
                'size': item.size,
                'amount': item.amount,
                'price': item.price
            })
        sell_list.append({
            'state': 'pending',
            'date': sell.date_posted,
            'total': sell.total,
            'details': details_list
        })

    for sell in sells:
        details_list = []
        details = CloseSellDetails.objects.filter(sell=sell.id)
        for item in details:
            details_list.append({
                'product': item.product_name,
                'size': item.size,
                'amount': item.amount,
                'price': item.price
            })
        sell_list.append({
            'state': 'close',
            'date': sell.date_posted,
            'shipping': sell.shipping,
            'total': sell.total,
            'details': details_list
        })

    return JsonResponse({'sell_list': sell_list})

