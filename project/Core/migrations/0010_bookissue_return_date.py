# Generated by Django 5.1.3 on 2024-12-16 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0009_alter_bookissue_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookissue',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]