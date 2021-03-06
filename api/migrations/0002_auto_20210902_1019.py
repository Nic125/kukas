# Generated by Django 3.1.6 on 2021-09-02 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sell',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='sell',
            name='product_id',
        ),
        migrations.CreateModel(
            name='CloseSellDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(default=100, max_length=20)),
                ('size', models.CharField(default=0, max_length=20)),
                ('amount', models.CharField(default=0, max_length=20)),
                ('price', models.CharField(default=0, max_length=20)),
                ('date_posted', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('sell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sell')),
            ],
            options={
                'verbose_name': 'Detalle compra',
                'verbose_name_plural': 'Detalles compras',
            },
        ),
    ]
