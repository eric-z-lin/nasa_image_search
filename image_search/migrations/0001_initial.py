# Generated by Django 2.1.7 on 2019-03-18 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nasa_id', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': 'images',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_query', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': 'searches',
            },
        ),
    ]
