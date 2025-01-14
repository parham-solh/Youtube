from django.db import models
from PIL import Image
from uuid import uuid4
from django.utils.html import format_html
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_child_products(self):
       
        childs = self.children.all()
        child_products = VIDEO.objects.filter(category__in=childs)
        own_products = VIDEO.objects.filter(category=self)
        all_products = child_products | own_products
        return all_products.distinct()


class VIDEO(models.Model):
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.PROTECT, related_name="videos"
    )
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="thumbnails")
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    description = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    count_like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def thumbnail_preview(self):
        
        if self.thumbnail:
            return format_html(
                f"<img src='{self.thumbnail.url}' alt='{self.title}' width='100' height='60' >"
            )
        return "null"
    thumbnail_preview.short_description = "thumbnail_preview"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # تغییر اندازه تصویر بندانگشتی
        if self.thumbnail:
            img = Image.open(self.thumbnail.path)

            # تنظیم سایز تصویر
            max_size = (720, 404)  # سایز استاندارد (عرض، ارتفاع)
            img.thumbnail(max_size)

            # ذخیره تصویر تغییر اندازه داده‌شده
            img.save(self.thumbnail.path)


class Comment(models.Model):
    video = models.ForeignKey(
        VIDEO, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"comment for : {self.video.title}"
