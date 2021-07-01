from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'shop/index.html')

def about(request):
    return render(request,'shop/about.html')

def contact(request):
    return render(request,'shop/index.html')

def productview(request):
    return render(request,'shop/index.html')

def search(request):
    return render(request,'shop/index.html')

def tracker(request):
    return render(request,'shop/index.html')

def checkout(request):
    return render(request,'shop/index.html')
