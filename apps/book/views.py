from rest_framework.viewsets import ModelViewSet
from  rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import PostBook
from .serializers import PostBookSerializer
from cloudinary.uploader import upload
from  .api_cloudinary import api_cloudinary
api_cloudinary()

def upload_image_post(image):
        """
        subir imagen a cloudinary
        """
        try:
            upload_result = upload(image, folder='uploadPost')
            return upload_result
        except Exception as e:
            print(f"Error subiendo la imagen: {str(e)}")

            raise e

class PostBookViewSet(ModelViewSet):
    """
    CRUD para un post de libros
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PostBook.objects.all()
    serializer_class = PostBookSerializer
   

class UploadView(APIView):
    """
    clase de prueba para subir la imagen
    """
    def post(self, request):
        # Revisa si se está recibiendo el archivo de imagen
        if 'image' not in request.FILES:
            return Response({"error": "No se encontró ninguna imagen en la solicitud"}, status=status.HTTP_400_BAD_REQUEST)
        
        image = request.FILES.get('image')

        try:
            # Revisa si el archivo se está recibiendo correctamente
            print(f"Archivo recibido: {image.name}, tamaño: {image.size}")

            # Supón que upload_image_post es una función que sube la imagen a algún servicio
            upload_result = upload_image_post(image)

            return Response({
                "message": "Imagen subida con éxito", 
                "url": upload_result
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        

