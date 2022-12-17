# Generated by Django 3.2.16 on 2022-11-27 15:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_page_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='users',
            field=models.ManyToManyField(null=True, related_name='favorite_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
