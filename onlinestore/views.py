from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'onlinestore/index.html')

def contact(request):
    return render(request,'onlinestore/contact.html')
def about(request):
    return render(request,'onlinestore/about.html')
def shop(request):
    return render(request,'onlinestore/shop.html')