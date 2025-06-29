import json
import os
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from django.urls import reverse_lazy
from .models import Product, Category
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .services import ProductService


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')

        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        context.update(json_data)

        return context


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


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        return super().form_valid(form)


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

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.groups.filter(
            name='Product moderator group').exists()


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'catalog.can_delete_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.groups.filter(
            name='Product moderator group').exists()


class PublishProductView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, owner=request.user)
        product.is_published = True
        product.save()
        return redirect('product_list')


class UnpublishProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.user == product.owner or request.user.groups.filter(name='Product moderator group').exists():
            product.is_published = False
            product.save()
            return redirect('product_list')
        else:
            return HttpResponseForbidden("У вас нет прав для отмены публикации этого продукта.")

    def test_func(self):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return self.request.user == product.owner or self.request.user.groups.filter(
            name='Product moderator group').exists()


class ProductsInCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_in_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Возвращает список всех продуктов в указанной категории."""
        category_pk = self.kwargs['pk']
        return ProductService.get_products_by_category(category_pk)

    def get_context_data(self, **kwargs):
        """Добавляет объект категории в контекст."""
        context = super().get_context_data(**kwargs)
        category_pk = self.kwargs['pk']
        context['category'] = get_object_or_404(Category, pk=category_pk)
        return context
