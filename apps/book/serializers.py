from rest_framework import serializers
from django.db.transaction import atomic
from django.db import IntegrityError
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

    def validateData(self, value, message):
        if not value: 
           raise serializers.ValidationError({'message': message})
        return

    def validate(self, data):
        instance = self.instance
        image = data.get('image', instance.image_url if instance else None)
        name_book = data.get('name', instance.name if instance else None)
        author = data.get('author', instance.author if instance else None)
        category = data.get('category', instance.category if instance else None)
        status = data.get('status', instance.status if instance else None)
        exhange_type = data.get('exhange_type', instance.exhange_type if instance else None)

        self.validateData(image, 'La imagen obligatoria')
        self.validateData(name_book, 'El nombre del libro obligatorio')
        self.validateData(author, 'El author del libro obligatorio')
        self.validateData(category, 'La categoria para el libro obligatorio')
        self.validateData(status, 'El estado del libro es obligatorio')
        self.validateData(exhange_type, 'El tipo de cambio de libros obligatorio')

        return data

    @atomic
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        request_user = self.context['request'].user
        validated_data['user'] = request_user

        if image:
            try:
                #llamada para subir la imagen a Cloudinary
                upload_result = self.upload_image_post(image)

                #verificar si url y public_id fueren devueltos
                image_url = upload_result.get('url')
                image_id = upload_result.get('public_id')

                if not image_url or not image_id:
                    raise serializers.ValidationError('Error al obtener la URL o ID de la imagen.')

                # Asignar image_url e image_id al validated_data
                validated_data['image_url'] = image_url
                validated_data['image_id'] = image_id

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
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['creation_date'] = instance.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        representation['update_date'] = instance.update_date.strftime('%Y-%m-%d %H:%M:%S')
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBook
        fields = ['id', 'name', 'description', 'creation_date', 'update_date']
        read_only_fields = ['id', 'creation_date', 'update_date']

    def validate(self, data):
        instance = self.instance
        name = data.get('name', instance.name if instance else None)
        description = data.get('description', instance.description if instance else None)

        if not CategoryBook.objects.filter(name__iexact=name).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError({'message': 'El nombre ya esta en uso'})
        return data

    def create(self, validated_data):
        try:
            category = CategoryBook.objects.create(**validated_data)
            return category
        except ValueError as e:
            raise serializers.ValidationError({f'Erro de valir: {str(e)}'})
        except IntegrityError as e:
            raise serializers.ValidationError({f'Error de integridad: {str(e)}'})
        except Exception as e:
            raise serializers.ValidationError(f"Ocurrió un error al crear la categoría: {str(e)}")
        
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['creation_date'] = instance.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        representation['update_date'] = instance.update_date.strftime('%Y-%m-%d %H:%M:%S')
        return representation

class ExchangeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeType
        fields = ['id', 'name', 'description', 'creation_date', 'update_date']
        read_only_fields = ['id', 'creation_date', 'update_date']

    def validate(self, data):
        instance = self.instance
        name = data.get('name', instance.name if instance else None)
        description = self.data.get('description', instance.description if instance else None)

        if not ExchangeType.objects.filter(name__iexact=name).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError({'message': 'Nombre en uso'})

    @atomic
    def create(self, validated_data):
        try:
            tipe = ExchangeType.objects.create(**validated_data)
            return tipe
        except ValueError as e:
            raise serializers.ValidationError({f'Erro de valir: {str(e)}'})
        except IntegrityError as e:
            raise serializers.ValidationError({f'Error de integridad: {str(e)}'})
        except Exception as e:
            raise serializers.ValidationError(f"Ocurrió un error al crear la categoría: {str(e)}")

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['creation_date'] = instance.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        representation['update_date'] = instance.update_date.strftime('%Y-%m-%d %H:%M:%S')
        return representation

class BooskStatusSerializer(serializers.ModelSerializer): pass