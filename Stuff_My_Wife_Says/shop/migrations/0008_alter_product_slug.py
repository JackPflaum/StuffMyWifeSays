# Generated by Django 4.2.2 on 2023-08-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_alter_shoppingcartsession_cart_uuid_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
