from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        if obj.views_count == 100:
            send_mail(
                'Поздравление! Ваша статья достигла 100 просмотров',
                f'Статья "{obj.title}" теперь имеет 100 просмотров.',
                'from@example.com',  # Используйте свой адрес электронной почты
                ['to@example.com'],  # Замените на адрес, на который хотите отправить уведомление
            )
        obj.save()
        return obj

class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview_image', 'is_published']
    success_url = reverse_lazy('blog_list')

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
