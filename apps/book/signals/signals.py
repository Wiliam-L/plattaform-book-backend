from django.db.models.signals import post_migrate
from django.dispatch import receiver
from ..models import CategoryBook, ExchangeType

@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name == 'apps.book':
        # Crear categorías de libros
        categories = [
            "Ficción",
            "No Ficción",
            "Ciencia Ficción",
            "Fantástica",
            "Misterio",
            "Biografía",
            "Historia",
            "Autoayuda",
            "Romance",
            "Thriller",
            "Literatura Clásica",
            "Infantil",
            "Juvenil",
            "Poesía",
            "Ensayo",
            "Viajes",
            "Cocina",
            "Desarrollo Personal",
            "Tecnología",
            "Salud"
        ]
        
        for category in categories:
            CategoryBook.objects.get_or_create(name=category, defaults={'description': ''})

        # Crear tipos de intercambio
        exchange_types = [
            'gratis',
            'intercambio',
        ]

        for name in exchange_types:
            ExchangeType.objects.get_or_create(name=name, defaults={'description': ''})
