# Generated by Django 5.0.3 on 2024-03-11 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_contents'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='title',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
