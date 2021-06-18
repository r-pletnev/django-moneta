# Generated by Django 3.2.3 on 2021-05-30 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneta', '0002_load_payment_systems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentsystem',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('merchant_id', models.CharField(help_text='MNT_ID', max_length=30)),
                ('transaction_id', models.CharField(max_length=255, unique=True)),
                ('operation_id', models.CharField(blank=True, null=True, help_text='MNT_OPERATION_ID', max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, help_text='MNT_AMOUNT', max_digits=11)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('currency', models.CharField(help_text='MNT_CURRENCY_CODE', max_length=3)),
                ('test_mode', models.BooleanField(help_text='MNT_TEST_MODE')),
                ('signature', models.CharField(blank=True, help_text='MNT_SIGNATURE', max_length=250)),
                ('payment_system_unit_id', models.CharField(help_text='paymentSystem.unitId', max_length=10, blank=True)),
                ('corraccount', models.CharField(blank=True, null=True, help_text='MNT_CORRACCOUNT', max_length=20)),
                ('subscriber_id', models.PositiveIntegerField(blank=True, help_text='MNT_SUBSCRIBER_ID', null=True)),
                ('status', models.CharField(choices=[('CHECK', 'CHECK'), ('PAID', 'PAID')], max_length=6)),
                ('payment_system', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='moneta.paymentsystem')),
            ],
            options={
                'db_table': 'mnt_invoices',
            },
        ),
    ]
