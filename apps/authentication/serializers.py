from .models import CustomUser, EmailVerification, IconPerfil
from rest_framework import serializers, status
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import uuid

class IconPefilSerializer(serializers.ModelSerializer):
    class Meta:
        model = IconPerfil
        fields = ['id', 'image', 'name']
 
class CustomUserSerializer(serializers.ModelSerializer): 
    icon = IconPefilSerializer(required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'icon']

        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True}
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserSerializer, self).__init__(*args, **kwargs)

        if self.instance:
            for field in ['username', 'email', 'password']:
                self.fields[field].required = False
                self.fields[field].allowed_blank = True

    def validate(self, data):
        instance = self.instance
        username = data.get('username')
        email = data.get('email')

        #create/post
        if not instance:
            if username and CustomUser.objects.filter(username=username).exists():
                raise serializers.ValidationError({'error': 'nombre de usuario ya en uso.'})

            if email and CustomUser.objects.filter(email=email).exists():
                raise serializers.ValidationError({'error': 'correo ya esta registrado o en uso'})
        else: pass

        return data
    
    @transaction.atomic
    def create(self, validated_data):
        icon_data = validated_data.pop('icon', None)
        password = validated_data['password']
        is_superuser = validated_data.pop('is_superuser', False)
        user = CustomUser.objects.create(**validated_data)
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()

        if icon_data:
            icon = IconPerfil.objects.create(**icon_data)
            user.icon = icon
            user.save()

        verification_code = uuid.uuid4()
        expiration_time = timezone.now() + timedelta(hours=24)
        EmailVerification.objects.create(user=user, code=verification_code, expiration_date=expiration_time) 

        # Llama correctamente al método estático
        CustomUserSerializer.send_verification_email(email=user.email, code=verification_code)
        
        return user

    @staticmethod
    def send_verification_email(email, code):
        subject = 'Verificación de correo electrónico'
        message = f'Tu código de verificación es: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        try:
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            raise serializers.ValidationError({'error': f'Error al enviar el correo: {str(e)}'})


class EmailVerificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = EmailVerification
        fields = ['user', 'code', 'expiration_date', 'verificated']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.user: representation['user'] = {instance.user.username, instance.user.email}

        return representation

   