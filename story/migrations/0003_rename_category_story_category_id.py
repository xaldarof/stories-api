# Generated by Django 4.2 on 2023-04-15 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_alter_story_category_delete_storycategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='category',
            new_name='category_id',
        ),
    ]
