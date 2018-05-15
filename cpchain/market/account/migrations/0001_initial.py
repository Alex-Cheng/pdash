# Generated by Django 2.0.3 on 2018-05-15 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('public_key', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
        migrations.CreateModel(
            name='WalletUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=200, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('active_date', models.DateTimeField(auto_now_add=True, verbose_name='active date')),
                ('status', models.IntegerField(default=0, verbose_name='0:normal,1:frozen,2:suspend,3.deleted')),
            ],
            options={
                'ordering': ('created', 'public_key'),
            },
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='account.WalletUser', verbose_name='WalletUser'),
        ),
    ]
