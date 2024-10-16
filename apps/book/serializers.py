from rest_framework import serializers
from django.db.transaction import atomic
from .models import BookStatus, CategoryBook, ExchangeType, PostBook, CustomUser
from cloudinary.uploader import upload
from  .api_cloudinary import api_cloudinary
api_cloudinary()

class PostBookSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = PostBook
        fields = ['user', 'image_url', 'image_id', 'name', 'author', 'category', 'status', 'exhange_type']
        read_only_fields = ['creation_date', 'update_date']

    def __init__(self, *args, **kwargs):
        super(PostBookSerializer, self).__init__(*args, **kwargs)

        #si es un put entonces se acepta campos en blanco
        if self.instance:
            for field in ['image_url', 'image_id', 'name', 'author', 'category', 'status', 'exhange_type']:
                self.fields[field].required = False
                self.fields[field].allow_blank = True
    
    def validate(self, data):
        instance = self.instance
        image = data.get('image')

        if not instance:
            if not image: raise serializers.ValidationError({"message": "imagen obligatorio"})
        
        return data

    @atomic
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        request_user = self.context['request'].user
        validated_data['user'] = request_user
        if image:
            try:
                upload_result = self.upload_image_post(image)
                validated_data['image_url'] = upload_result.get('url')
                validated_data['image_id'] = upload_result.get('public_id')

                postBook = PostBook.objects.create(**validated_data)
                postBook.save()
                return postBook
            except Exception as e: raise serializers.ValidationError(f'error al subir la imagen')

        raise serializers.ValidationError('imagen es obligatoria para crear el post')

    def upload_image_post(self, image):
        """
        subir imagen a cloudinary
        """
        try:
            upload_result = upload(image, folder='uploadPost')
            return upload_result
        except Exception as e:
            print(f"Error subiendo la imagen: {str(e)}")

            raise e


class CategorySerializer(serializers.ModelSerializer):
    pass

class ExchangeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeType
        fields = ['id', 'name', 'description', 'creation_date', 'update_date']
        read_only_fields = ['id', 'creation_date', 'update_date']

class BooskStatusSerializer(serializers.ModelSerializer): pass