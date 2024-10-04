from django.contrib import admin
from .models import BookStatus, CategoryBook, ExchangeType, PostBook

# Register your models here.
admin.site.register(BookStatus)
admin.site.register(CategoryBook)
admin.site.register(ExchangeType)
admin.site.register(PostBook)