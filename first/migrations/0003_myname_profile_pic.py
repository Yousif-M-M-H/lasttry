# Generated by Django 4.1 on 2022-09-02 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0002_remove_myname_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='myname',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
