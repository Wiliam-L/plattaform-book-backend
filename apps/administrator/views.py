from apps.book.serializers import PostBookSerializer, PostBook
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

class PostBookViewSet(viewsets.ModelViewSet): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = PostBook.objects.all()
    serializer_class = PostBookSerializer
    http_method_names = ['get', 'delete']


