# Generated by Django 3.2.16 on 2022-11-26 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['page_number']},
        ),
    ]
