import json
from django.shortcuts import redirect, render
from . models import *
from django.http import JsonResponse
from django.db.models import Sum
import qrcode
from django.core.files.base import ContentFile
from PIL import Image
import io
from django.contrib.auth import authenticate, login 


def MenuView(request):
    items = MenuItem.objects.all()
    context = {'items': items}
    return render(request,'menu.html' , context)

def EditMenu(request):
    caty = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        cat_id = request.POST.get('cat')
        img = request.FILES.get('image')
        cat = Category.objects.get(id = cat_id)
        new_item = MenuItem(name = name , description = desc, price = price, img= img)
        new_item.save()
        new_item.category.set([cat])

    context = {'caty': caty}
    return render(request , 'Additem.html' , context)


def OrderGet(request , pk):
    items = MenuItem.objects.all()
    table_no = pk # Each url has a unique int primary key and each table no is associated with that.
    request.session['table_no'] = table_no # use request.seesion here as i wanted to use this table_no
    # later in the updateorder function this make my variable tabe_no available for other function.
    context = {'items': items , 'id': pk}
    return render(request,'order.html' , context)

def ConfirmOrder(request , pk):
     t_no = pk
     order = Order.objects.filter(table_no = pk)

     total = Order.objects.filter(table_no=t_no).aggregate(Sum('price'))['price__sum']
     context = {'order': order , 'total' : total , 'id': pk}
     return render(request , 'confirm_order.html' , context)

def DelItem(request , pk):
    obj = Order.objects.filter(id = pk).first()
   
    if obj.quantity > 1:
         unit_price = obj.price / obj.quantity
         print('unit_price: ' , unit_price)
         obj.quantity -= 1
         obj.price = unit_price * obj.quantity
         obj.save()
    else:
        obj.delete()
        
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)

def navbar(request):
    return render(request , 'main.html')


def UpdateItem(request ):
    data = json.loads(request.body)
    ItemId = data['itemId']
    Action = data['action']

    total = 0
    item = MenuItem.objects.get(id=ItemId)
    table_no = request.session['table_no']
    order = Order.objects.filter(items=item , table_no = table_no).first()
    if order:
        order.quantity += 1
        order.price = item.price * order.quantity
        order.save()
        
    else:
        order = Order.objects.create(items=item, price=item.price, quantity=1 , table_no = request.session['table_no']) 

        
    total = Order.objects.filter(table_no=table_no).aggregate(Sum('price'))['price__sum']
    return JsonResponse({'message': 'Item was added', 'total': total}, safe=False)


def ConfirmedOrd(request):
     all_orders = Order.objects.all()
     total = 0
     total = Order.objects.aggregate(Sum('price'))['price__sum']
     order_by_table = {}
     for order in all_orders:
        if order.table_no in order_by_table:
            order_by_table[order.table_no].append(order)
        else:
            order_by_table[order.table_no] = [order]
    
     context = {'order_by_table': order_by_table , 'total' : total}
     return render(request , 'confirmed_ord.html' , context)



def CompletedOrder(request , pk):
    obj = Order.objects.filter(table_no = pk)
    obj.delete()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)


def EditItem(request , pk):
    caty = Category.objects.all()
    if request.user.is_authenticated:
        item = MenuItem.objects.get(id = pk)
        if request.method == 'POST':
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            price = request.POST.get('price')
            cat_id = request.POST.get('cat')
            img = request.FILES.get('image')
            cat = Category.objects.get(id=cat_id)
            item.name = name
            item.description = desc
            item.price = price
            item.img = img
            item.save()
            item.category.set([cat])

            previous_page = request.META.get('HTTP_REFERER', '/')
            return redirect(previous_page)
            

    context = {'Item': item , 'caty': caty}
    return render(request,'Edit_Item.html' , context)

def RemoveItem(request , pk):
    Item = MenuItem.objects.get(id = pk)
    Item.delete()
    previous_page = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_page)



def DashBoard(request):
    return render(request , 'dashboard.html')


def QR_Gen(data):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border =4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black' , back_color='white')
    return img

def QR(request):
    if request.method == 'POST':
        data = request.POST.get('user_url')
        img = QR_Gen(data)
        image_io = io.BytesIO()
        img.save(image_io , format='PNG')
        image_file = ContentFile(image_io.getvalue() , name='table_qrcode.png')
        qr_image = QRGen.objects.create(imag = image_file)
        context = {'img':qr_image }
        return render(request,'QR.html' , context)
    return render(request , 'QR.html')

def Thanks(request):
    return render(request , 'Thanks.html')


def Login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=user, password=password)
        if user:
            login(request, user)    
            return redirect('dash')

    return render(request , 'login.html')

    
