# Generated by Django 4.2 on 2023-04-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0013_alter_storyview_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_frozen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='story',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
    ]