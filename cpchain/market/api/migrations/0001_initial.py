# Generated by Django 2.0.3 on 2018-03-30 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_address', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('expired_date', models.DateTimeField(null=True, verbose_name='date expired')),
                ('verify_code', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WalletUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('active_date', models.DateTimeField(auto_now_add=True, verbose_name='active date')),
                ('status', models.IntegerField(default=0, verbose_name='0:normal,1:frozen,2:suspend,3.deleted')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.WalletUser'),
        ),
    ]