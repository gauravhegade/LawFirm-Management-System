# Generated by Django 5.1.1 on 2024-10-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawyer_app', '0008_document_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(default='IDK', upload_to='documents/'),
            preserve_default=False,
        ),
    ]