from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders
from math import ceil
import json

# Create your views here.
def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, nSlides), nSlides])

        # params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
        # allProds = [[products, range(1, nSlides), nSlides],
        #             [products, range(1, nSlides), nSlides]]

        params = {'allProds': allProds}
    return render(request, "shop/index.html", params)

  



def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html")



def search(request):
    return render(request, "shop/search.html")

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, "shop/prodView.html", {'product': product[0]})

def checkout(request):

    thank=False  

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " "  + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        amount = request.POST.get('amount', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()    
        thank = True
        idnew = order.order_id
        allProds = Product.objects.values('product_name', 'price')
        allProdsh = Product.objects.values('id')
        return render(request, "shop/checkout.html", {'thank':thank, 'idnew':idnew, 'allProds':json.dumps(list(allProds)), 'allProdsh':allProdsh})
        #request paytm to transfer the amount to your account after payment by user
        param_dict = {
           "requestType"   : "Payment",
          "mid"           : "YOUR_MID_HERE",
            "websiteName"   : "WEBSTAGING",
          "orderId"       : order.order_id,
          "callbackUrl"   : "https://127.0.0.1:8000/shop/handlerequest/",
          "txnAmount"     : {
          "value"     : amount,
          "currency"  : "INR",
          },
           "userInfo"      : {
           "custId"    : email,
            },
          }
        
        param_dict['CHECKSUMHASH'] = Checksum.generate.checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict':param_dict})
        return render(request, "shop/checkout.html", {'allProds':json.dumps(list(allProds)), 'allProdsh':allProdsh})




    allProds = Product.objects.values('product_name', 'price')
    allProdsh = Product.objects.values('id')
    # params = {'allProds':json.dumps(list(allProds)), 'allProdsh':allProdsh, 'thank':thank}
    params = {'allProds':json.dumps(list(allProds)), 'allProdsh':allProdsh}
 

    return render(request, "shop/checkout.html", params)

