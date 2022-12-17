from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core import validators
from unidecode import unidecode
from django.template.defaultfilters import slugify


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if username is None:
            raise TypeError('Users must have a username')

        if email is None:
            raise TypeError('Users must have an email address')

        if password is None:
            raise TypeError('Users must have a password')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_staff_user(self, username, email, password):
        if username is None:
            raise TypeError('Superuser must have a username')

        if email is None:
            raise TypeError('Superuser must have an email address')

        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError('Superuser must have a username')

        if email is None:
            raise TypeError('Superuser must have an email address')

        if password is None:
            raise TypeError('Superuser must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('Author', 'Author'),
        ('Reader', 'Reader'),
    )
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(unique=True, validators=[validators.validate_email], db_index=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=ROLES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


# class FavoriteBooks(models.ManyToManyRel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
#     book = models.ForeignKey('Book', on_delete=models.CASCADE, blank=True)
#

class Book(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=False, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='favorite_books', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class Page(models.Model):
    book = models.ForeignKey(Book, related_name='pages', on_delete=models.CASCADE)
    content = models.TextField()
    page_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['page_number']
        unique_together = ['book', 'page_number']

    def __str__(self):
        return str(self.page_number)
