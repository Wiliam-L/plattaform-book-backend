from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from datetime import timedelta
import uuid
from django.utils import timezone

class IconPerfil(models.Model):
    image = models.ImageField(upload_to='icons/')
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'icon_perfil'
    
    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff=True
        user.is_active=True
        user.save()
        return user

    class Meta:
        db_table = 'custom_user_manager'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    icon = models.ForeignKey(IconPerfil, on_delete=models.SET_NULL, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'custom_user'

    def __str__(self):
        return self.email

class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4) 
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()  
    verificated = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_verification'

    def __str__(self):
        return f'{self.user.email} - {self.code}'

    @classmethod
    def create_or_update_verification(cls, user, validity_period=30):
        """
        Crea o actualiza un código de verificación. El código tiene un tiempo de vida definido por `validity_period` en horas.
        """
        # Verificar si ya existe un código de verificación no verificado
        existing_verification = cls.objects.filter(user=user, verificated=False).first()
        
        # Tiempo de expiración (ejemplo 24 horas)
        expiration_time = timezone.now() + timedelta(minutes=validity_period)

        if existing_verification:
            # Si existe, actualiza el código y el tiempo de expiración
            existing_verification.code = uuid.uuid4()
            existing_verification.expiration_date = expiration_time
            existing_verification.save()
            return existing_verification
        else:
            # Si no existe, crea un nuevo registro
            return cls.objects.create(user=user, expiration_date=expiration_time)
    
    def is_code_valid(self):
        """
        Verifica si el código es válido (no expirado).
        """
        return timezone.now() < self.expiration_date and not self.verificated

