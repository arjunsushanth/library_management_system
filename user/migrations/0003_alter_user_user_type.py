# Generated by Django 4.2.2 on 2023-07-06 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_user_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('member', 'MEMBER'), ('librarian', 'LIBRARIAN')], max_length=250),
        ),
    ]