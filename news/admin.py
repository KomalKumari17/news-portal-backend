from django.contrib import admin
from .models import Category, Area, News, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Area)
admin.site.register(News)
admin.site.register(Comment)
