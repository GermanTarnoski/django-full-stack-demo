from django.urls import path, include
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="main_index", ),
    path('movimientos/list/', MovimientosBancariosListView.as_view(), name='movimientos_list'),
    path('usuario/new/', UsuarioNuevoView.as_view(), name='main_nuevo_usuario'),
    path('usuario/detail/<int:pk>/update/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuario/detail/<int:pk>/', UsuarioDeleteView.as_view(), name='usuario_vista'),
    path('usuarios/', UsuariosListView.as_view(), name='usuarios_lista'),
    path('banco/new/', BancoNuevoView.as_view(), name='main_nuevo_banco'),
    path('banco/detail/<int:pk>/update/', BancoUpdateView.as_view(), name='banco_update'),
    path('banco/detail/<int:pk>/', BancoDeleteView.as_view(), name='banco_vista'),
    path('bancos/', BancosListView.as_view(), name='bancos_lista'),
    path('cuentascorrientes/new/', CuentasCorrientesNuevoView.as_view(), name='main_nuevo_cuentascorrientes'),
    path('cuentascorrientes/detail/<int:pk>/update/', CuentasCorrientesUpdateView.as_view(), name='cuentascorrientes_update'),
    path('cuentascorrientes/detail/<int:pk>/', CuentasCorrientesDeleteView.as_view(), name='cuentascorrientes_vista'),
    path('cuentascorrientes/', CuentasCorrientesListView.as_view(), name='cuentascorrientes_lista'),

]
