# Generated manually for slug fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_ourservice_description_ourservice_icon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Slug'),
        ),
        migrations.AddField(
            model_name='ourservice',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='Slug'),
        ),
    ]

