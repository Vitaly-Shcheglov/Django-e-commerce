from django.views.generic import ListView, DetailView, View, CreateView
from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()

class ContactView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class AddProductView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'image', 'category']
    template_name = 'catalog/add_product.html'

    def get_success_url(self):
        return redirect('home')
