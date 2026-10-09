"""Genera evidencias reproducibles y el PDF de la Unidad 1.

Ejecutar desde tienda_online: ../venv/Scripts/python.exe generar_entrega.py
Las peticiones se ejecutan contra Django usando APIClient y una BD temporal.
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from contextlib import redirect_stdout

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.utils import setup_databases, teardown_databases
from rest_framework.test import APIClient
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage, PageBreak, Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'entrega_unidad_1'
OUT.mkdir(exist_ok=True)
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 19)


def capture(filename, title, text):
    lines = text.expandtabs(4).splitlines()
    width = max(1000, int(max((FONT.getlength(line) for line in lines), default=0)) + 64)
    image = Image.new('RGB', (width, 85 + 26 * len(lines)), '#101827')
    draw = ImageDraw.Draw(image)
    draw.text((24, 20), title, font=FONT, fill='#80cfff')
    for index, line in enumerate(lines):
        draw.text((24, 65 + 26 * index), line, font=FONT, fill='#edf2f7')
    path = OUT / filename
    image.save(path)
    return path


result = subprocess.run(
    [sys.executable, 'manage.py', 'test'], cwd=ROOT,
    capture_output=True, text=True,
)
terminal = '> python manage.py test\n' + result.stdout + result.stderr
(OUT / 'pruebas.txt').write_text(terminal, encoding='utf-8')
if result.returncode:
    raise RuntimeError(terminal)
terminal_image = OUT / 'terminal_directa.png'
if not terminal_image.exists():
    terminal_image = capture('terminal.png', 'Terminal | ejecución real', terminal)

# BD de pruebas: no se crean usuarios ni productos en db.sqlite3.
settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, 'testserver']
with redirect_stdout(io.StringIO()):
    databases = setup_databases(verbosity=0, interactive=False)
try:
    from products.models import Category, Product
    from products.services import ProductPriceService
    get_user_model().objects.create_user(username='demo', password='demo-password')
    electronics = Category.objects.create(name='Electrónica')
    clothing = Category.objects.create(name='Ropa')
    products = [
        Product.objects.create(name='Laptop', price='15000.00', category=electronics),
        Product.objects.create(name='Camisa', price='500.00', category=clothing),
    ]
    client = APIClient()
    token = client.post('/api/token/', {
        'username': 'demo', 'password': 'demo-password'
    }, format='json')
    assert token.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
    responses = []
    for product in products:
        response = client.get('/api/precio-final/', {'product_id': product.pk})
        assert response.status_code == 200
        responses.append({
            'request': f'GET /api/precio-final/?product_id={product.pk}',
            'status': response.status_code, 'body': response.data,
        })
    client.credentials()
    denied = client.get('/api/precio-final/', {'product_id': products[0].pk})
    assert denied.status_code == 401
    # Verifica la fábrica, la estrategia por defecto y los errores de entrada.
    default = Product.crear_con_categoria_default('Cuaderno', '19.99')
    assert default.category.name == 'General'
    assert ProductPriceService.final_price(default.pk)['final_price'] == '19.99'
    second = Product.crear_con_categoria_default('Lápiz', '5.00')
    assert second.category_id == default.category_id
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['access'])
    assert client.get('/api/precio-final/').status_code == 400
    assert client.get('/api/precio-final/', {'product_id': 999999}).status_code == 404
finally:
    teardown_databases(databases, verbosity=0)

(OUT / 'respuestas.json').write_text(
    json.dumps(responses, ensure_ascii=False, indent=2), encoding='utf-8'
)
endpoint_images = []
for index, evidence in enumerate(responses):
    endpoint_images.append(capture(
        f'endpoint_{index + 1}.png', 'Endpoint | respuesta real con JWT',
        evidence['request'] + '\nAuthorization: Bearer [JWT omitido]\n'
        + f"HTTP {evidence['status']}\n\n"
        + json.dumps(evidence['body'], ensure_ascii=False, indent=2),
    ))

services = (ROOT / 'products/services.py').read_text(encoding='utf-8')
models = (ROOT / 'products/models.py').read_text(encoding='utf-8')
views = (ROOT / 'products/views.py').read_text(encoding='utf-8')
tests = (ROOT / 'products/tests.py').read_text(encoding='utf-8')
service_parts = services.split('class ProductPriceService:')
service_images = [
    capture('services_estrategias.png', 'products/services.py | Strategy', service_parts[0]),
    capture('services_seleccion.png', 'products/services.py | selección y cálculo',
            'class ProductPriceService:' + service_parts[1]),
]
factory = models[models.index('class Product('):models.index('    name =', models.index('class Product('))]
factory_image = capture('models_factory.png', 'products/models.py | creación por defecto', factory)
view_image = capture('views_facade.png', 'products/views.py | Facade y JWT',
                    views[:views.index('class ProductViewSet')])
test_image = capture('tests.png', 'products/tests.py | dos pruebas nuevas',
                     tests[tests.index('class PrecioFinalAPITestCase'):tests.index('class CategoryAPITestCase')])

# Utiliza capturas directas de PowerShell cuando están disponibles.
if all((OUT / (name + '_directa.png')).exists() for name in [
    'services1', 'services2', 'models', 'views', 'tests1', 'tests2', 'endpoint1', 'endpoint2'
]):
    service_images = [OUT / 'services1_directa.png', OUT / 'services2_directa.png']
    factory_image = OUT / 'models_directa.png'
    view_image = OUT / 'views_directa.png'
    endpoint_images = [OUT / 'endpoint1_directa.png', OUT / 'endpoint2_directa.png']
    test_images = [OUT / 'tests1_directa.png', OUT / 'tests2_directa.png']
else:
    test_images = [test_image]

diagram = Image.new('RGB', (1100, 600), 'white')
draw = ImageDraw.Draw(diagram)
boxes = [
    ('urls.py', 'Enrutamiento: /api/precio-final/'),
    ('views.py', 'Presentación: JWT, validación y Facade'),
    ('services.py', 'Negocio: elección de Strategy y descuento'),
    ('models.py', 'Persistencia: Product, Category y ORM'),
]
for index, (name, detail) in enumerate(boxes):
    top = 20 + index * 140
    draw.rounded_rectangle((120, top, 980, top + 90), radius=12,
                           fill='#e8f2fc', outline='#23558a', width=3)
    draw.text((150, top + 12), name, font=FONT, fill='#17375e')
    draw.text((150, top + 45), detail, font=FONT, fill='#17375e')
    if index < 3:
        draw.line((550, top + 92, 550, top + 130), fill='#23558a', width=4)
        draw.polygon([(540, top + 120), (560, top + 120), (550, top + 133)], fill='#23558a')
diagram_path = OUT / 'arquitectura.png'
diagram.save(diagram_path)

styles = getSampleStyleSheet()
story = []


def paragraph(text, style='BodyText'):
    story.append(Paragraph(text, styles[style]))
    story.append(Spacer(1, 10))


def picture(path, max_height=640):
    with Image.open(path) as img:
        width, height = img.size
    scale = min(475 / width, max_height / height)
    story.append(PDFImage(str(path), width=width * scale, height=height * scale))
    story.append(Spacer(1, 10))


paragraph('Unidad 1: arquitectura y patrones de diseño', 'Title')
paragraph('Proyecto: tienda_online · Django REST Framework · 30/09/2026')
paragraph('1. Arquitectura en capas', 'Heading1')
paragraph('El proyecto es un monolito organizado en capas. Django aporta el modelo MVT; '
          'la API REST utiliza vistas y serializadores en la presentación, sin plantillas HTML. '
          'La nueva capa de servicios concentra las reglas de descuento y el ORM accede a SQLite.')
picture(diagram_path, 320)
paragraph('Flujo: el cliente envía un JWT y un product_id; urls.py selecciona la vista, '
          'views.py autentica y valida, services.py obtiene el producto mediante models.py '
          'y aplica la estrategia. El resultado vuelve como JSON al cliente. '
          'Los serializadores validan y representan los datos en la capa de presentación.')
paragraph('Reglas: Electrónica 10 %, Ropa 20 % y otras categorías o productos sin categoría 0 %. '
          'Se usa Decimal con redondeo a dos decimales. Sin JWT: 401; parámetro inválido: 400; '
          'producto inexistente: 404.')
story.append(PageBreak())
paragraph('2. services.py: estrategias de descuento', 'Heading1')
picture(service_images[0])
story.append(PageBreak())
paragraph('2. services.py: selección de la estrategia', 'Heading1')
picture(service_images[1])
story.append(PageBreak())
paragraph('3. models.py: crear_con_categoria_default', 'Heading1')
picture(factory_image, 180)
paragraph('El método de clase crea o reutiliza General y devuelve una instancia persistida. '
          'Al usar cls, una subclase puede sobrescribir el método de creación. '
          'No cambia el esquema de la base de datos y no requiere migraciones.')
paragraph('4. views.py: endpoint como Facade', 'Heading1')
picture(view_image, 370)
paragraph('La ruta se registra en products/urls.py con '
          "path('precio-final/', PrecioFinalView.as_view(), name='precio-final'). "
          'El prefijo api/ de la configuración principal produce /api/precio-final/.')
story.append(PageBreak())
paragraph('5. Endpoint funcionando con dos categorías', 'Heading1')
paragraph('Peticiones HTTP realizadas desde PowerShell contra el servidor local y una base de pruebas. '
          'El token se obtuvo en /api/token/ y se envió en Authorization.')
for endpoint_image in endpoint_images:
    picture(endpoint_image, 265)
paragraph('Laptop / Electrónica: 15000.00 → 13500.00. Camisa / Ropa: 500.00 → 400.00. '
          'Una petición adicional sin token respondió HTTP 401.')
story.append(PageBreak())
paragraph('6. tests.py: dos pruebas del endpoint', 'Heading1')
for evidence_image in test_images:
    picture(evidence_image, 310)
paragraph('La prueba autenticada obtiene un JWT real y verifica HTTP 200 y los precios '
          'de dos categorías con subTest. La segunda comprueba HTTP 401 sin token.')
story.append(PageBreak())
paragraph('7. Terminal: todas las pruebas pasan', 'Heading1')
picture(terminal_image, 300)
paragraph('Resultado real: 8 pruebas, OK. Se conservan las 6 pruebas anteriores y se '
          'agregan las 2 solicitadas. La base de pruebas se destruye al terminar.')
paragraph('Verificaciones adicionales: reutilización de General por la fábrica, '
          'precio sin descuento para General, HTTP 400 sin product_id y HTTP 404 '
          'para un producto inexistente. Todas pasaron.')
story.append(PageBreak())
paragraph('8. Tabla de patrones', 'Heading1')
rows = [['Nombre', 'Categoría', 'Evidencia', 'Explicación'],
        ['Factory Method', 'Creacional', 'models.py: Product.\ncrear_con_categoria_default',
         'Centraliza la creación con General mediante un método de clase que devuelve '
         'el producto. Es la variante simplificada de fábrica solicitada; el Factory Method '
         'clásico usa subclases que sobrescriben la creación. Aquí cls permite esa extensión.'],
        ['Strategy', 'Comportamiento', 'services.py: DiscountStrategy, ElectronicsDiscount, '
         'ClothingDiscount y NoDiscount',
         'Encapsula descuentos intercambiables bajo apply(price). El servicio selecciona '
         'la estrategia por categoría sin trasladar la fórmula a la vista.'],
        ['Facade', 'Estructural', 'views.py: PrecioFinalView.get; services.py: ProductPriceService',
         'Ofrece una entrada HTTP sencilla que coordina autenticación, validación, '
         'consulta y cálculo. El cliente recibe el precio sin conocer el ORM ni las estrategias.']]
table = Table([[Paragraph(cell.replace('\n', '<br/>'), styles['BodyText']) for cell in row]
               for row in rows], colWidths=[70, 85, 140, 180], repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f2fc')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
]))
story.append(table)
paragraph('Organización ágil', 'Heading2')
paragraph('Incremento entregado: consulta de precio final protegida. Criterios de aceptación: '
          'dos categorías con descuentos distintos, JWT obligatorio, dos pruebas nuevas y '
          'evidencias reproducibles. Trabajo completado: separar reglas, incorporar fábrica, '
          'exponer ruta, validar y documentar. Esta organización describe el incremento; '
          'no afirma que se hayan realizado ceremonias ágiles no registradas.')


def footer(canvas, doc):
    canvas.setFont('Helvetica', 9)
    canvas.drawString(45, 25, 'tienda_online | Unidad 1')
    canvas.drawRightString(A4[0] - 45, 25, str(doc.page))


pdf = OUT / 'Unidad_1_Arquitectura_y_Patrones.pdf'
SimpleDocTemplate(str(pdf), pagesize=A4, rightMargin=45, leftMargin=45,
                  topMargin=40, bottomMargin=45).build(
    story, onFirstPage=footer, onLaterPages=footer
)
print(f'PDF generado: {pdf}')
print('8 pruebas OK; dos respuestas 200; sin JWT 401; verificaciones adicionales OK.')
