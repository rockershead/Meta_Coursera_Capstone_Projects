from django.contrib import admin

# Register your models here.

from .models import Category,MenuItem,Cart

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)