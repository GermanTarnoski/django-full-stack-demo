# Generated by Django 4.0.4 on 2022-06-14 03:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_pedido_articulos_remove_pedido_cantidad_orden_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avisos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('documento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CuentasCorrientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cuenta', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('cuit', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MovimientosBancarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clasificacion', models.CharField(max_length=50)),
                ('es_error', models.BooleanField(default=False)),
                ('fecha', models.DateField(verbose_name=datetime.datetime(2022, 6, 14, 0, 56, 3, 813648))),
                ('concepto', models.CharField(max_length=50)),
                ('importe', models.FloatField()),
                ('descripcion_ampliada', models.CharField(max_length=50)),
                ('comprobante', models.CharField(max_length=50)),
                ('saldo', models.FloatField()),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.cuentascorrientes')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientosErp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('clasificacion', models.CharField(max_length=50)),
                ('numero_asiento', models.IntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('debe', models.FloatField()),
                ('haber', models.FloatField()),
                ('saldo', models.FloatField()),
                ('razon_social_cliente_proveedor', models.CharField(max_length=50)),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.cuentascorrientes')),
            ],
        ),
        migrations.CreateModel(
            name='Responsables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('cargo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SaldosBancarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name=datetime.datetime(2022, 6, 14, 0, 56, 3, 812646))),
                ('importe', models.FloatField()),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.cuentascorrientes')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.CharField(max_length=50)),
                ('usuario', models.CharField(max_length=50)),
                ('banco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.banco')),
            ],
        ),
        migrations.RemoveField(
            model_name='direccion',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='articulo',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='direccion',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='orden',
        ),
        migrations.DeleteModel(
            name='Articulo',
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='Direccion',
        ),
        migrations.DeleteModel(
            name='Fabrica',
        ),
        migrations.DeleteModel(
            name='Orden',
        ),
        migrations.DeleteModel(
            name='Pedido',
        ),
        migrations.AddField(
            model_name='movimientoserp',
            name='responsable',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.responsables'),
        ),
        migrations.AddField(
            model_name='movimientosbancarios',
            name='responsable',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.responsables'),
        ),
        migrations.AddField(
            model_name='cuentascorrientes',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usuario'),
        ),
        migrations.AddField(
            model_name='banco',
            name='empresas',
            field=models.ManyToManyField(to='main.empresa'),
        ),
        migrations.AddField(
            model_name='avisos',
            name='responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.responsables'),
        ),
    ]