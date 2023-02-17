from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.urls import reverse

# Create your models here.


class Empresa(models.Model):
    descripcion = models.CharField(max_length=50)
    cuit = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)


class Banco(models.Model):
    empresas = models.ManyToManyField(Empresa)
    descripcion = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('banco_vista', kwargs={'pk': self.pk})


class BancoForm(ModelForm):
    class Meta:
        model = Banco
        fields = ['empresas', 'descripcion']


class Usuario(models.Model):
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    documento = models.IntegerField()
    usuario = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('usuario_vista', kwargs={'pk': self.pk})


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['banco', 'documento', 'usuario', 'empresa']


class CuentasCorrientes(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    numero_cuenta = models.IntegerField()

    def get_absolute_url(self):
        return reverse('cuentascorrientes_vista', kwargs={'pk': self.pk})


class CuentasCorrientesForm(ModelForm):
    class Meta:
        model = CuentasCorrientes
        fields = ['usuario', 'numero_cuenta']


class SaldosBancarios(models.Model):
    cuenta = models.OneToOneField(CuentasCorrientes, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.localtime().now())
    importe = models.FloatField(null=False)


class Responsables(models.Model):
    email = models.EmailField(max_length=100)
    cargo = models.CharField(max_length=50)


class MovimientosBancarios(models.Model):
    responsable = models.ForeignKey(Responsables, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(CuentasCorrientes, on_delete=models.CASCADE)
    clasificacion = models.CharField(max_length=50)
    es_error = models.BooleanField(default=False)
    fecha = models.DateField(default=timezone.localtime().now())
    concepto = models.CharField(max_length=50)
    importe = models.FloatField(null=False)
    descripcion_ampliada = models.CharField(max_length=250)
    comprobante = models.CharField(max_length=50)
    saldo = models.FloatField(null=False)


class MovimientosBancariosForm(ModelForm):
    class Meta:
        model = MovimientosBancarios
        fields = ['responsable', 'cuenta', 'clasificacion', 'es_error', 'fecha', 'concepto', 'importe', 'descripcion_ampliada', 'comprobante', 'saldo']


class MovimientosErp(models.Model):
    cuenta = models.ForeignKey(CuentasCorrientes, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.localtime().now())
    responsable = models.ForeignKey(Responsables, on_delete=models.CASCADE)
    clasificacion = models.CharField(max_length=100)
    numero_asiento = models.PositiveIntegerField()
    es_error = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=100)
    debe = models.FloatField(null=False)
    haber = models.FloatField(null=False)
    saldo = models.FloatField(null=False)
    razon_social_cliente_proveedor = models.CharField(max_length=50)


class MovimientosErpForm(ModelForm):
    class Meta:
        model = MovimientosErp
        fields = ['cuenta', 'fecha', 'responsable', 'clasificacion', 'numero_asiento', 'descripcion', 'debe', 'haber', 'saldo', 'razon_social_cliente_proveedor']


class Avisos(models.Model):
    asunto = models.CharField(max_length=100)
    responsable = models.ForeignKey(Responsables, on_delete=models.CASCADE)
