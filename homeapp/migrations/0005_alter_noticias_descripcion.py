# Generated by Django 4.2.5 on 2023-11-15 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0004_alter_noticias_shared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticias',
            name='descripcion',
            field=models.CharField(max_length=500),
        ),
    ]