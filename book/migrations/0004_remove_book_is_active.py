# Generated by Django 4.2.2 on 2023-07-06 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='is_active',
        ),
    ]
