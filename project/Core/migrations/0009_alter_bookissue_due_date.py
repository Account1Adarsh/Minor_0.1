# Generated by Django 5.1.3 on 2024-12-16 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0008_remove_bookissue_return_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
