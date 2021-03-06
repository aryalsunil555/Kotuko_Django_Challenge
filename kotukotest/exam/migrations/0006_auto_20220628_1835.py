# Generated by Django 3.2 on 2022-06-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_todolist_uploaded_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AlterField(
            model_name='todolist',
            name='image',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
