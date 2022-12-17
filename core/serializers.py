from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Book, Page
from django.contrib.auth.models import Group


class PageSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field="slug", queryset=Book.objects.all())

    class Meta:
        model = Page
        fields = ['book', 'page_number', 'content']
        extra_kwargs = {
            'url': {'lookup_field': 'page_number'}
        }


class BookSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Book
        fields = ['name', 'slug', 'author', 'created_at', 'updated_at', 'pages']
        read_only_fields = ['author']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class MyBookSerializer(BookSerializer):
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['name', 'slug', 'author', 'created_at', 'updated_at', 'users', 'pages']


class AuthorsSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['username', 'books']
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        role = self.validated_data['role']
        try:
            group = Group.objects.get(name=role)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "Такой Роли не существует"})

        if password != password2:
            raise serializers.ValidationError({"detail": "Пароли не совпадают"})
        user.set_password(password)
        user.save()
        user.groups.add(group)
        return user


