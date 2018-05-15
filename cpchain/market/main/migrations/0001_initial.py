# Generated by Django 2.0.3 on 2018-05-14 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.CharField(max_length=256, verbose_name='image url')),
                ('link', models.CharField(max_length=256, verbose_name='link address')),
                ('index', models.IntegerField(default=0, verbose_name='sort by index')),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='HotTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=256, verbose_name='image url')),
                ('tag', models.CharField(max_length=256, verbose_name='tag')),
                ('index', models.IntegerField(default=0, verbose_name='sort by index')),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.CharField(max_length=256, verbose_name='image url')),
                ('link', models.CharField(max_length=256, verbose_name='link address')),
                ('index', models.IntegerField(default=0, verbose_name='sort by index')),
                ('status', models.IntegerField(default=1)),
            ],
        ),
    ]
