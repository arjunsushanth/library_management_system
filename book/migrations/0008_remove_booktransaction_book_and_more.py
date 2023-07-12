# Generated by Django 4.2.2 on 2023-07-11 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_alter_borrowedbook_approval_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booktransaction',
            name='book',
        ),
        migrations.AddField(
            model_name='booktransaction',
            name='borrowed_book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transcation_borrowedbook', to='book.borrowedbook'),
        ),
    ]