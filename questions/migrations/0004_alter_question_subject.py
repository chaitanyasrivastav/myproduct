# Generated by Django 3.2 on 2022-08-30 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_delete_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subject',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
