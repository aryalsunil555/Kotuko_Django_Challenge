# Generated by Django 3.2 on 2022-06-27 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_alter_todolist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
