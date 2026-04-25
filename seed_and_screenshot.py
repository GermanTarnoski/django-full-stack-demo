"""
Seed the database with sample data, start the dev server, and take screenshots.
"""
import os
import sys
import django
import subprocess
import time
import signal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django101.settings')
sys.path.insert(0, '/home/user/django-full-stack-demo')
django.setup()

from django.contrib.auth.models import User
from main.models import (
    Empresa, Banco, Usuario, CuentasCorrientes, SaldosBancarios,
    Responsables, MovimientosBancarios, MovimientosErp, Avisos
)
from datetime import date

# ── Seed ────────────────────────────────────────────────────────────────────

# Auth user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

# Companies
emp1 = Empresa.objects.get_or_create(descripcion='Construcciones del Sur S.A.', cuit='30-71234567-8', telefono='011-4555-1234')[0]
emp2 = Empresa.objects.get_or_create(descripcion='Logística Norte S.R.L.', cuit='30-68901234-5', telefono='011-4666-5678')[0]

# Banks
banco1 = Banco.objects.get_or_create(descripcion='Banco Nación Argentina')[0]
banco1.empresas.set([emp1, emp2])
banco2 = Banco.objects.get_or_create(descripcion='Banco Santander')[0]
banco2.empresas.set([emp1])

# Operators (usuarios de banco)
op1 = Usuario.objects.get_or_create(banco=banco1, documento=32456789, usuario='Laura Gómez', empresa=emp1)[0]
op2 = Usuario.objects.get_or_create(banco=banco1, documento=28901234, usuario='Martín Rodríguez', empresa=emp2)[0]
op3 = Usuario.objects.get_or_create(banco=banco2, documento=35678901, usuario='Ana Fernández', empresa=emp1)[0]

# Accounts
cc1 = CuentasCorrientes.objects.get_or_create(usuario=op1, numero_cuenta=10023456)[0]
cc2 = CuentasCorrientes.objects.get_or_create(usuario=op2, numero_cuenta=10034567)[0]
cc3 = CuentasCorrientes.objects.get_or_create(usuario=op3, numero_cuenta=20011234)[0]

# Balances
SaldosBancarios.objects.get_or_create(cuenta=cc1, defaults={'importe': 854320.50})
SaldosBancarios.objects.get_or_create(cuenta=cc2, defaults={'importe': 215780.00})

# Responsible parties
resp1 = Responsables.objects.get_or_create(email='pgonzalez@empresa.com', cargo='Analista Contable')[0]
resp2 = Responsables.objects.get_or_create(email='jlopez@empresa.com', cargo='Supervisor de Tesorería')[0]

# Bank movements
bank_mvs = [
    dict(responsable=resp1, cuenta=cc1, clasificacion='Crédito', es_error=False,
         fecha=date(2025, 3, 5), concepto='Cobro cliente', importe=125000.00,
         descripcion_ampliada='Pago factura #A-0042 Construcciones del Sur', comprobante='REC-1001', saldo=854320.50),
    dict(responsable=resp1, cuenta=cc1, clasificacion='Débito', es_error=False,
         fecha=date(2025, 3, 8), concepto='Pago proveedor', importe=-43200.00,
         descripcion_ampliada='OP #502 Materiales de construcción', comprobante='OP-502', saldo=811120.50),
    dict(responsable=resp2, cuenta=cc2, clasificacion='Crédito', es_error=True,
         fecha=date(2025, 3, 10), concepto='Transferencia entrante', importe=80000.00,
         descripcion_ampliada='Transferencia sin comprobante registrado en sistema', comprobante='TRF-2201', saldo=295780.00),
    dict(responsable=resp1, cuenta=cc1, clasificacion='Débito', es_error=False,
         fecha=date(2025, 3, 12), concepto='Débito bancario', importe=-1850.00,
         descripcion_ampliada='Comisión mantenimiento cuenta corriente', comprobante='CMN-0031', saldo=809270.50),
    dict(responsable=resp2, cuenta=cc2, clasificacion='Crédito', es_error=False,
         fecha=date(2025, 3, 15), concepto='Cobro cliente', importe=54000.00,
         descripcion_ampliada='Pago factura #B-0118 Logística Norte', comprobante='REC-1002', saldo=349780.00),
    dict(responsable=resp1, cuenta=cc3, clasificacion='Débito', es_error=True,
         fecha=date(2025, 3, 18), concepto='Cheque debitado', importe=-22500.00,
         descripcion_ampliada='Cheque #004521 sin contrapartida en ERP', comprobante='CHQ-4521', saldo=187600.00),
]
for mv in bank_mvs:
    MovimientosBancarios.objects.get_or_create(**mv)

# ERP movements
erp_mvs = [
    dict(cuenta=cc1, fecha=date(2025, 3, 5), responsable=resp1, clasificacion='Ingresos por ventas',
         numero_asiento=8801, es_error=False, descripcion='Cobro factura cliente',
         debe=0, haber=125000.00, saldo=854320.50, razon_social_cliente_proveedor='Construcciones del Sur S.A.'),
    dict(cuenta=cc1, fecha=date(2025, 3, 8), responsable=resp1, clasificacion='Compras y gastos',
         numero_asiento=8802, es_error=False, descripcion='Pago a proveedor de materiales',
         debe=43200.00, haber=0, saldo=811120.50, razon_social_cliente_proveedor='Aceros del Plata S.A.'),
    dict(cuenta=cc2, fecha=date(2025, 3, 10), responsable=resp2, clasificacion='Transferencias',
         numero_asiento=8803, es_error=True, descripcion='Transferencia sin documentación',
         debe=0, haber=80000.00, saldo=295780.00, razon_social_cliente_proveedor='Desconocido'),
    dict(cuenta=cc1, fecha=date(2025, 3, 12), responsable=resp1, clasificacion='Gastos bancarios',
         numero_asiento=8804, es_error=False, descripcion='Comisión bancaria',
         debe=1850.00, haber=0, saldo=809270.50, razon_social_cliente_proveedor='Banco Nación Argentina'),
    dict(cuenta=cc2, fecha=date(2025, 3, 15), responsable=resp2, clasificacion='Ingresos por ventas',
         numero_asiento=8805, es_error=False, descripcion='Cobro factura cliente',
         debe=0, haber=54000.00, saldo=349780.00, razon_social_cliente_proveedor='Logística Norte S.R.L.'),
    dict(cuenta=cc3, fecha=date(2025, 3, 18), responsable=resp1, clasificacion='Cheques emitidos',
         numero_asiento=8806, es_error=True, descripcion='Cheque sin registrar en banco',
         debe=22500.00, haber=0, saldo=187600.00, razon_social_cliente_proveedor='Proveedor XYZ S.R.L.'),
]
for mv in erp_mvs:
    MovimientosErp.objects.get_or_create(**mv)

print("Seeding complete.")

# ── Start server ─────────────────────────────────────────────────────────────

server = subprocess.Popen(
    [sys.executable, 'manage.py', 'runserver', '--noreload', '8765'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    cwd='/home/user/django-full-stack-demo'
)
time.sleep(3)
print("Server started.")

# ── Screenshots ───────────────────────────────────────────────────────────────

os.makedirs('/home/user/django-full-stack-demo/screenshots', exist_ok=True)

import playwright
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:8765'

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    page = ctx.new_page()

    # Log in silently
    page.goto(f'{BASE}/accounts/login/')
    page.wait_for_load_state('networkidle')
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin123')
    page.click('button[type="submit"], input[type="submit"]')
    page.wait_for_load_state('networkidle')

    # 1. Home dashboard
    page.goto(f'{BASE}/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/home/user/django-full-stack-demo/screenshots/01_home.png', full_page=True)
    print("Screenshot: home")

    # 2. Movements / reconciliation page
    page.goto(f'{BASE}/movimientos/list/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/home/user/django-full-stack-demo/screenshots/02_movimientos.png', full_page=True)
    print("Screenshot: movimientos")

    # 3. Banks list
    page.goto(f'{BASE}/bancos/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/home/user/django-full-stack-demo/screenshots/03_bancos.png', full_page=True)
    print("Screenshot: bancos")

    # 4. Operators list
    page.goto(f'{BASE}/usuarios/')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/home/user/django-full-stack-demo/screenshots/04_usuarios.png', full_page=True)
    print("Screenshot: usuarios")

    browser.close()

server.terminate()
server.wait()
print("Done.")
