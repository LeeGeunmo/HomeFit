# Generated by Django 5.0.6 on 2024-06-06 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0005_alter_exerciseset_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseset',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
