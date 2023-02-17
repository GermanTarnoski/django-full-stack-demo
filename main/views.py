from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import *
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):  # Página principal
    template_name = 'main/index.html'


class MovimientosBancariosListView(View):  # Lista de movimientos, tanto erp como de banco
    template_name = "main/movimientos_list.html"

    def get(self, *args, **kwargs):
        """ Obtiene los datos de los movimientos y los despliega en dos listas. Una para movimientos de sistema
        y otra para movimientos del banco."""

        movimientosbancarios = MovimientosBancarios.objects.all()
        movimientoserp = MovimientosErp.objects.all()

        """ Las listas tienen opcción de filtrar por responsables y empresas, así que se obtienen
        todos los objetos de esos modelos para mostrarse en las listas de opciones para filtrar """
        responsables = Responsables.objects.all()
        empresas = Empresa.objects.all()

        context = {'movimientosbancarios': movimientosbancarios, 'movimientoserp': movimientoserp,
                   'responsables': responsables, 'empresas': empresas}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        """ Obtiene las opciones elegidas en los filtros y trae los datos de movimientos que correspondan.
        Al filtrar por empresa, el formulario devuelve un campo 'empresa' pero no devuelve 'responsable', y viceversa.
        Eso es porque solo se puede filtrar de a una opción."""
        if 'empresa' in self.request.POST:
            if self.request.POST['empresa'] == '':
                movimientosbancarios = MovimientosBancarios.objects.all()
                movimientoserp = MovimientosErp.objects.all()
            else:
                movimientosbancarios = MovimientosBancarios.objects.filter(
                    cuenta__usuario__empresa__id=self.request.POST['empresa']) # se trae la empresa correspondiente
                # al ID que se eligió en el formulario.
                movimientoserp = MovimientosErp.objects.filter(
                    cuenta__usuario__empresa__id=self.request.POST['empresa'])
        elif 'responsable' in self.request.POST:
            if self.request.POST['responsable'] == '':
                movimientosbancarios = MovimientosBancarios.objects.all()
                movimientoserp = MovimientosErp.objects.all()
            else:
                movimientosbancarios = MovimientosBancarios.objects.filter(
                    responsable__id=self.request.POST['responsable'], es_error=1) # se traen los movimientos que son errores y del responsable seleccionado.
                movimientoserp = MovimientosErp.objects.filter(responsable__id=self.request.POST['responsable'],
                                                               es_error=1)
        responsables = Responsables.objects.all()
        empresas = Empresa.objects.all()

        form = MovimientosBancariosForm(self.request.POST)

        if form.is_valid():

            context = {'movimientosbancarios': movimientosbancarios, 'movimientoserp': movimientoserp,
                       'responsables': responsables, 'empresas': empresas} # se lleva el contenido solicitado

            return render(self.request, self.template_name, context)

        else:
            return render(self.request, self.template_name,
                          {'form': form, 'movimientosbancarios': movimientosbancarios, 'movimientoserp': movimientoserp,
                           'responsables': responsables, 'empresas': empresas})


# region Ingreso, actualización, borrado y detalle de usuarios
# ingreso
class UsuarioNuevoView(View):
    template_name = 'main/usuario_nuevo.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de bancos y empresas y los despliega en el formulario para elegirlos como opción de asociación
        del usuario"""
        bancos = Banco.objects.all()
        empresas = Empresa.objects.all()

        context = {'bancos': bancos, 'empresas': empresas}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        bancos = Banco.objects.all()
        empresas = Empresa.objects.all()

        form = UsuarioForm(self.request.POST)

        if form.is_valid():
            # se obtienen los datos ingresados en el formulario y se genera el nuevo usuario
            nuevo_usuario = Usuario()
            nuevo_usuario.banco = form.cleaned_data['banco']
            nuevo_usuario.documento = form.cleaned_data['documento']
            nuevo_usuario.usuario = form.cleaned_data['usuario']
            nuevo_usuario.empresa = form.cleaned_data['empresa']

            nuevo_usuario.save()

            return redirect('usuario_vista', pk=nuevo_usuario.id) # Cuando el usuario fue generado, se muestra la vista en detalle del usuario.
        else:
            return render(self.request, self.template_name, {'form': form, 'bancos': bancos, 'empresas': empresas})


# actualización
class UsuarioUpdateView(View):

    template_name = 'main/usuario_update.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de un usuario identificado por su ID y los despliega en el formulario """

        instance = get_object_or_404(Usuario, pk=self.kwargs['pk']) # se buscan los datos del usuario con el private key correspondiente
        form = UsuarioForm(instance=instance) # se genera un formulario de usuario con los datos correspondientes traídos en la línea anterior

        bancos = Banco.objects.all() # tal vez se busca modificar el banco asociado o la empresa entonces se traen todos para usar de opciones.
        empresas = Empresa.objects.all()

        context = {'form': form,
                   'usuario': instance,
                   'bancos': bancos,
                   'empresas': empresas}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        instance = get_object_or_404(Usuario, pk=self.kwargs['pk'])
        form = UsuarioForm(self.request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('usuario_vista', pk=instance.id) # cuando se mandan los datos y la actualización es exitosa, se ve la vista detalle del usuario.
        else:
            context = {
                'usuario': instance,
                'form': form
            }
            return render(self.request, self.template_name, context)


# detalle y borrado
class UsuarioDeleteView(View):

    def get(self, *args, **kwargs):
        """ Obtiene el modelo y muestra el html de confirmación """

        usuario = get_object_or_404(Usuario, pk=kwargs['pk']) # se obtienen los detalles del usuario que se quiere ver, actualizar o eliminar
        cuentascorrientes = list(CuentasCorrientes.objects.filter(usuario=usuario)) # se traen las cuentas corrientes del usuario
        context = {'usuario': usuario, 'cuentascorrientes': cuentascorrientes}

        return render(self.request, 'main/usuario_vista.html', context)

    def post(self, *args, **kwargs):
        """ El botón "editar" en el formulario lleva a la vista de actualización.
        El botón "Eliminar" elimina un registro de la DB y es el que funciona como post"""

        usuario = get_object_or_404(Usuario, pk=kwargs['pk'])
        usuario.delete()

        return redirect('usuarios_lista') # cuando fue eliminado se redirige a la vista de lista.


# lista
class UsuariosListView(ListView):
    model = Usuario


# endregion


# region Ingreso, actualización, borrado y detalle de bancos


# ingreso
class BancoNuevoView(View):
    template_name = 'main/banco_nuevo.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de empresas y los despliega en el formulario para elegirlos como opción de asociación
        del banco"""
        empresas = Empresa.objects.all()

        context = {'empresas': empresas}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        empresas = Empresa.objects.all()

        form = BancoForm(self.request.POST)

        if form.is_valid():
            # se obtienen los datos ingresados en el formulario y se genera el nuevo usuario

            lista = self.request.POST.getlist(
                'empresas')  # se obtiene una lista de empresas, porque en el formulario pueden elegirse varias.

            nuevo_banco = Banco()
            nuevo_banco.descripcion = form.cleaned_data['descripcion']
            nuevo_banco.save()

            # para asociar al banco las empresas elegidas, primero hubo que crear el nuevo banco y
            # después iterar para agregar cada empresa a la lista de empresas del banco.
            # esto es así por la naturaleza de la relación Many-to-Many.

            for id_empresa in lista:
                emp = Empresa.objects.get(pk=id_empresa)
                nuevo_banco.empresas.add(emp)

            return redirect('banco_vista', pk=nuevo_banco.id) # Cuando el banco fue generado, se muestra la vista en detalle del banco.
        else:
            return render(self.request, self.template_name, {'form': form, 'empresas': empresas})


# actualización
class BancoUpdateView(View):

    template_name = 'main/banco_update.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de un banco identificado por su ID y los despliega en el formulario """

        instance = get_object_or_404(Banco, pk=self.kwargs['pk']) # se buscan los datos del banco con el private key correspondiente
        form = BancoForm(instance=instance) # se genera un formulario de usuario con los datos correspondientes traídos en la línea anterior

        empresas = Empresa.objects.all() # tal vez se busca modificar la empresa asociada entonces se traen todas para usar de opciones.

        context = {'form': form,
                   'banco': instance,
                   'empresas': empresas}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        instance = get_object_or_404(Banco, pk=self.kwargs['pk'])
        form = BancoForm(self.request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('banco_vista', pk=instance.id) # cuando se mandan los datos y la actualización es exitosa, se ve la vista detalle del banco.
        else:
            context = {
                'banco': instance,
                'form': form
            }
            return render(self.request, self.template_name, context)


# borrado y detalle
class BancoDeleteView(View):

    def get(self, *args, **kwargs):
        """ Obtiene el modelo y muestra el html de confirmación """

        banco = get_object_or_404(Banco, pk=kwargs['pk'])
        context = {'banco': banco}

        return render(self.request, 'main/banco_vista.html', context)

    def post(self, *args, **kwargs):
        """ El botón "editar" en el formulario lleva a la vista de actualización.
        El botón "Eliminar" elimina un registro de la DB y es el que funciona como post"""

        banco = get_object_or_404(Banco, pk=kwargs['pk'])
        banco.delete()

        return redirect('bancos_lista') # cuando fue eliminado se redirige a la vista de lista.


class BancosListView(ListView):
    model = Banco


# endregion

# region Ingreso, actualización, borrado y detalle de cuentas


# ingreso
class CuentasCorrientesNuevoView(View):
    template_name = 'main/cuentascorrientes_nuevo.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de usuarios y los despliega en el formulario para elegirlos como opción de asociación
        de la cuenta corriente"""
        usuarios = Usuario.objects.all()

        context = {'usuarios': usuarios}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        usuarios = Usuario.objects.all()

        form = CuentasCorrientesForm(self.request.POST)

        if form.is_valid():
            # se obtienen los datos ingresados en el formulario y se genera el nuevo usuario

            nuevo_cuentas_corrientes = CuentasCorrientes()
            nuevo_cuentas_corrientes.numero_cuenta = form.cleaned_data['numero_cuenta']
            nuevo_cuentas_corrientes.usuario = form.cleaned_data['usuario']
            nuevo_cuentas_corrientes.save()

            return redirect('cuentascorrientes_vista', pk=nuevo_cuentas_corrientes.id) # Cuando la cuenta fue generada, se muestra la vista en detalle.
        else:
            return render(self.request, self.template_name, {'form': form, 'usuarios': usuarios})


# actualización
class CuentasCorrientesUpdateView(View):

    template_name = 'main/cuentascorrientes_update.html'

    def get(self, *args, **kwargs):
        """ Obtiene los datos de un CuentasCorrientes identificado por su ID y los despliega en el formulario """

        instance = get_object_or_404(CuentasCorrientes, pk=self.kwargs['pk']) # se buscan los datos de la cuenta con el private key correspondiente
        form = CuentasCorrientesForm(instance=instance) # se genera un formulario de cuentas corrientes con los datos correspondientes traídos en la línea anterior

        usuarios = Usuario.objects.all()# tal vez se busca modificar el usuario asociado entonces se traen todas para usar de opciones.

        context = {'form': form,
                   'cuentascorrientes': instance,
                   'usuarios': usuarios}

        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        instance = get_object_or_404(CuentasCorrientes, pk=self.kwargs['pk'])
        form = CuentasCorrientesForm(self.request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('cuentascorrientes_vista', pk=instance.id) # cuando se mandan los datos y la actualización es exitosa, se ve la vista detalle de la cuenta corriente.
        else:
            context = {
                'cuentascorrientes': instance,
                'form': form
            }
            return render(self.request, self.template_name, context)


# borrado y detalle
class CuentasCorrientesDeleteView(View):

    def get(self, *args, **kwargs):
        """ Obtiene el modelo y muestra el html de confirmación """

        cuentacorriente = get_object_or_404(CuentasCorrientes, pk=kwargs['pk'])
        context = {'cuentascorrientes':  cuentacorriente}

        return render(self.request, 'main/cuentascorrientes_vista.html', context)

    def post(self, *args, **kwargs):
        """ El botón "editar" en el formulario lleva a la vista de actualización.
        El botón "Eliminar" elimina un registro de la DB y es el que funciona como post"""

        cuentacorriente = get_object_or_404(CuentasCorrientes, pk=kwargs['pk'])
        cuentacorriente.delete()

        return redirect('cuentascorrientes_lista')# cuando fue eliminado se redirige a la vista de lista.


class CuentasCorrientesListView(ListView):
    model = CuentasCorrientes

# endregion
