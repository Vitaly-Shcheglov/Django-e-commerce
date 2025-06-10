from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blog_previews/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        permissions = (
            ('can_change_blogpost', 'Can change blog post'),
            ('can_delete_blogpost', 'Can delete blog post'),
            ('can_view_blogpost', 'Can view blog post'),
        )


    def __str__(self):
        return self.title
