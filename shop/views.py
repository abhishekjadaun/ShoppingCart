from django.db.models.expressions import Value
from django.shortcuts import render,HttpResponse
from shop.models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
import datetime
import stripe
from django.views.decorators.csrf import csrf_exempt # new


# Create your views here.
def index(request):
    # products= Product.objects.all()
    # n= len(products)
    # nSlides= n//4 + ceil((n/4) + (n//4))
    # params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'product': products}

    # cats = {item['category'] for item in catprods}
    #     for cat in cats:
    #         prod = Product.objects.filter(category=cat)
    #         n = len(prod)
    #         nSlides = n // 4 + ceil((n / 4) - (n // 4))
    #         allProds.append([prod, range(1, nSlides), nSlides])
        
    allProds=[]
    catProds=Product.objects.values('category','id').distinct()
    uniqueCategory=Product.objects.values('category').distinct()
    for i in  uniqueCategory:
        product=Product.objects.filter(category=i['category'])
        n = len(product)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([product, range(1, nSlides), nSlides])
    params={
             'allProds':allProds,
           }   
    return render(request,'shop/index.html',params)


def about(request):
    return render(request,'shop/about.html')


def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        created=datetime.date.today()
        contact=Contact(name=name,email=email,desc=desc,created=created)
        contact.save()
    return render(request,'shop/contact.html')


def productview(request,id):
    product=Product.objects.filter(id=id)
    params={
        'product':product[0]
    }
    return render(request,'shop/product-view.html',params)


def search(request):
    return render(request,'shop/index.html')


def tracker(request):
    if request.method=="POST":
        id=request.POST.get('id')
        email=request.POST.get('email')
        data=Order.objects.filter(id=id,email=email)
        if(len(data)>0):
            update=OrderUpdate.objects.filter(update_id=data[0].id)
            updateData=[]
            for item in update:
                updateData.append({'text':item.update_desc, 'time':item.timestamp})
           
            # params= [("item_data",updateData),("item_json",data[0].item_json)]
            params={
                'item_data':updateData,
                'item_json':json.loads(data[0].item_json),
            }

            return  HttpResponse(json.dumps(params,default=str))
        else:
            return HttpResponse('{}')

    return render(request,'shop/tracker.html')


def checkout(request):
    params={}
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        address=request.POST.get('address')
        state=request.POST.get('state')
        city=request.POST.get('city')
        zip=request.POST.get('zip')
        phone=request.POST.get('phone')
        item_json=request.POST.get('item_json')
        orders=Order(name=name,email=email,address=address,city=city, state=state,zip=zip,phone=phone,item_json=item_json)
        orders.save()
        update=OrderUpdate(update_id=orders.id,update_desc="Order has been Placed ")
        update.save()
        params={
            'id':orders.id,
            'success':'success',
        }
    return render(request,'shop/checkout.html',params)


@csrf_exempt
def payment(request,id):
    orderDetails=Order.objects.filter(id=id)
    item_json=json.loads(orderDetails[0].item_json)
    sum=0
    for key in item_json:
        sum=sum+item_json[key][0]*item_json[key][2]
    update=OrderUpdate(update_id=id,update_desc="Payment Confirmation Pending")
    update.save()
    params={
        'amount':sum,
        'id':id,
        'update_id':update.id
    }
  

    return render(request, 'shop/charge.html',params)

@csrf_exempt
def checkoutDirect(request,update_id,id,value):
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'      
    domain_url = scheme + request.get_host()+'/shop/'
    stripe.api_key =  "sk_test_51He27oKLe91aE5uB3bHKh0vyDRBRy5bGyAlT0lmcjy1J1e9T3maAWyjsh7B8xULp2gS1ml8CkjdgGPfIbbA4InWM00w0uds4Yr" # new
    try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}&update_id='+update_id,
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'order-'+id,
                        'quantity': 1,
                        'currency': 'INR',
                        'amount': int(float(value)*100)
,
                    }
                ]
              
            )
            return HttpResponse(json.dumps({'sessionId': checkout_session['id']},default=str))

    except Exception as e:
        return HttpResponse(json.dumps({'error': str(e)},default=str))

@csrf_exempt
def success(request):
    session_id=request.GET.get('session_id')
    update_id=request.GET.get('update_id')
    if session_id:

        update=OrderUpdate.objects.filter(id=update_id).update(update_desc='Your Order Has been Confirmed')
        print(update)
    params={
        'msg':'Your Order Has been Confirmed'
    }
    return render(request,'shop/success.html',params)

        





