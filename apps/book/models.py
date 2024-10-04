from django.db import models
from apps.authentication.models import CustomUser

#modelo para categorias de generos
class CategoryBook(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    creation_date =  models.DateTimeField(auto_now_add=True),
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

#tipo de intercambio ejem: gratis, intercambio
class ExchangeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    creation_date =  models.DateTimeField(auto_now_add=True),
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

#modelo para libro o para el post del mismo
class PostBook(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, related_name='posts')
    image_url = models.URLField()
    image_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ManyToManyField(CategoryBook, related_name='books')
    status = models.BooleanField(default=True)
    exhange_type = models.ForeignKey(ExchangeType, on_delete=models.PROTECT)
    creation_date =  models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'autor: {self.user.username} - libro: {self.name}'

#para saber si se llevo a cabo un intercambio
class BookStatus(models.Model):
    book = models.OneToOneField(PostBook, on_delete=models.CASCADE)
    book_exchange_status = models.BooleanField(default=False)
    creation_date =  models.DateTimeField(auto_now_add=True),
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'libro: {self.book.name} - intercambiado: {self.book_exchange_status}'
