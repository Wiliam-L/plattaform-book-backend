from django.contrib import admin
from .models import CustomUser, EmailVerification, IconPerfil

admin.site.register(CustomUser)
admin.site.register(EmailVerification)
admin.site.register(IconPerfil)
