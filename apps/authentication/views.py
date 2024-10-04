from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import CustomUserSerializer, EmailVerificationSerializer, IconPefilSerializer
from .models import CustomUser, EmailVerification, IconPerfil
import uuid 

class UserCreateView(generics.CreateAPIView): 
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            if user.is_active:
                try:
                    verification = EmailVerification.objects.get(user=user)
                    if verification.verificated:
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                            }, status=status.HTTP_200_OK)
                    else:                        
                        if verification.is_code_valid():
                            new_verification = EmailVerification.create_or_update_verification(verification.user)
                            getNewCode(code=new_verification.code, email=new_verification.user.email)
                            print("new code: ", new_verification.code)
                            return Response({
                                'message': 'El código ha expirado. Se ha enviado un nuevo código de verificación al correo.',
                            }, status=status.HTTP_401_UNAUTHORIZED)


                except EmailVerification.DoesNotExist:
                    return Response({
                        'message': 'No se encontró un registro de verificación'
                    }, status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({
                    'message': 'El usuario no está activo.'
                }, status=status.HTTP_403_FORBIDDEN)
                
        else:
            return Response({
                'message': 'Credenciales no válidas.',
            }, status=status.HTTP_401_UNAUTHORIZED)


class VeryEmailApiView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            verification = EmailVerification.objects.get(user_id=user)

            # Verificar si el código es válido y no ha expirado
            if user.is_active:
                if verification.verificated:
                    return Response({'message': 'La cuenta ya está activa'})
                
                if verification.is_code_valid():
                    if str(verification.code) == str(code):
                        #Marcar como verificado
                        verification.verificated = True
                        verification.save()
                        
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            'message': 'Cuenta activada',
                            'access': str(refresh.access_token),
                            'refresh': str(refresh)
                        }, status=status.HTTP_200_OK)

                    else:
                        return Response({
                            'message': 'Código inválido.'
                        }, status=status.HTTP_400_BAD_REQUEST)
                else: 
                    new_verification = EmailVerification.create_or_update_verification(verification.user)
                    getNewCode(code=new_verification.code, email=new_verification.user.email)
                    return Response({'message': "código expirado, se ha enviado uno nuevo"})
            else: return Response({"message", "No tienes acceso, por que tu cuenta esta suspendida"}, status=status.HTTP_403_FORBIDDEN)

        except EmailVerification.DoesNotExist:
            return Response({
                'message': 'No se encontró el registro de verificación.'
            }, status=status.HTTP_404_NOT_FOUND)

def getNewCode(code, email):
    CustomUserSerializer.send_verification_email(email=email, code=code)


class getUser(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class getEmailVerification(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = EmailVerification.objects.all()
    serializer_class = EmailVerificationSerializer


class getIcon(generics.ListAPIView):
    queryset = IconPerfil.objects.all()
    serializer_class = IconPefilSerializer