from django.contrib import admin

from .models import News, Sliders


# Модель товара
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'video', 'description', 'created', 'updated']


class SlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'video', 'description', 'created', 'updated']


admin.site.register(News, NewsAdmin)
admin.site.register(Sliders, SlideAdmin)