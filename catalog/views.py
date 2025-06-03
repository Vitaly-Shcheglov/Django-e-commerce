from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.urls import reverse_lazy
from .models import Product
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all()


class ContactView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
        else:
            return HttpResponse("Пожалуйста, заполните все поля!", status=400)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')


class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context
