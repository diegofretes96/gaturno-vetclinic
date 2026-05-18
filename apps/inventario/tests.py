from django.test import TestCase, Client
from django.urls import reverse
from .models import Categoria, Proveedor, Producto, MovimientoStock
from apps.accounts.models import Usuario


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_categoria(nombre='General'):
    cat, _ = Categoria.objects.get_or_create(nombre=nombre)
    return cat


def crear_proveedor():
    return Proveedor.objects.create(nombre='Distribuidora Vet S.A.')


def crear_producto(codigo='P001', nombre='Amoxicilina', stock=100, stock_min=10, **kwargs):
    cat = crear_categoria()
    defaults = dict(codigo=codigo, nombre=nombre, tipo='medicamento',
                    categoria=cat, unidad_medida='comp',
                    precio_venta=5000, stock_actual=stock, stock_minimo=stock_min)
    defaults.update(kwargs)
    return Producto.objects.create(**defaults)


class CategoriaModelTests(TestCase):
    def test_str(self):
        c = crear_categoria('Antibióticos')
        self.assertEqual(str(c), 'Antibióticos')

    def test_unico(self):
        Categoria.objects.create(nombre='Antibióticos')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nombre='Antibióticos')


class ProveedorModelTests(TestCase):
    def test_str(self):
        p = crear_proveedor()
        self.assertEqual(str(p), 'Distribuidora Vet S.A.')

    def test_activo_por_defecto(self):
        p = crear_proveedor()
        self.assertTrue(p.activo)


class ProductoModelTests(TestCase):
    def test_str(self):
        p = crear_producto()
        self.assertIn('Amoxicilina', str(p))
        self.assertIn('P001', str(p))

    def test_bajo_stock_false_cuando_stock_alto(self):
        p = crear_producto(stock=100, stock_min=10)
        self.assertFalse(p.bajo_stock)

    def test_bajo_stock_true_cuando_stock_igual_minimo(self):
        p = crear_producto(stock=10, stock_min=10)
        self.assertTrue(p.bajo_stock)

    def test_bajo_stock_true_cuando_stock_menor(self):
        p = crear_producto(stock=5, stock_min=10)
        self.assertTrue(p.bajo_stock)

    def test_activo_por_defecto(self):
        p = crear_producto()
        self.assertTrue(p.activo)

    def test_codigo_unico(self):
        crear_producto('COD001', 'Producto A')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            crear_producto('COD001', 'Producto B')

    def test_tipos_choices(self):
        tipos = [t[0] for t in Producto.TIPOS]
        self.assertIn('medicamento', tipos)
        self.assertIn('insumo', tipos)
        self.assertIn('vacuna', tipos)
        self.assertIn('alimento', tipos)

    def test_ordering_por_nombre(self):
        crear_producto('Z001', 'Zyrtec')
        crear_producto('A001', 'Amoxicilina B')
        qs = list(Producto.objects.all())
        self.assertLessEqual(qs[0].nombre, qs[-1].nombre)


class MovimientoStockModelTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.prod = crear_producto()

    def test_str(self):
        m = MovimientoStock.objects.create(producto=self.prod, tipo='entrada',
                                           cantidad=50, stock_anterior=100,
                                           stock_resultante=150, usuario=self.u)
        s = str(m)
        self.assertIn('Entrada', s)
        self.assertIn('Amoxicilina', s)

    def test_tipos_choices(self):
        tipos = [t[0] for t in MovimientoStock.TIPOS]
        self.assertIn('entrada', tipos)
        self.assertIn('salida', tipos)
        self.assertIn('ajuste', tipos)
        self.assertIn('vencimiento', tipos)


class InventarioViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.prod = crear_producto()

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('inventario:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_busqueda(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:lista'), {'q': 'Amoxicilina'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Amoxicilina')

    def test_lista_filtro_tipo(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:lista'), {'tipo': 'medicamento'})
        self.assertEqual(r.status_code, 200)

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:detalle', args=[self.prod.pk]))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        cat = crear_categoria('Nueva Cat')
        data = {'codigo': 'P999', 'nombre': 'Ibuprofeno', 'tipo': 'medicamento',
                'categoria': cat.pk, 'unidad_medida': 'comp',
                'precio_costo': '1000', 'precio_venta': '2000',
                'stock_actual': '0', 'stock_minimo': '5',
                'requiere_receta': False, 'descripcion': '', 'activo': True}
        r = self.client.post(reverse('inventario:crear'), data)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Producto.objects.filter(codigo='P999').exists())

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:editar', args=[self.prod.pk]))
        self.assertEqual(r.status_code, 200)

    def test_movimiento_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:movimiento'))
        self.assertEqual(r.status_code, 200)

    def test_movimiento_entrada_actualiza_stock(self):
        self.client.force_login(self.u)
        stock_inicial = self.prod.stock_actual
        data = {'producto': self.prod.pk, 'tipo': 'entrada',
                'cantidad': '50', 'motivo': 'Compra'}
        r = self.client.post(reverse('inventario:movimiento'), data)
        self.assertEqual(r.status_code, 302)
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock_actual, stock_inicial + 50)

    def test_movimiento_salida_reduce_stock(self):
        self.client.force_login(self.u)
        stock_inicial = self.prod.stock_actual
        data = {'producto': self.prod.pk, 'tipo': 'salida',
                'cantidad': '20', 'motivo': 'Dispensación'}
        r = self.client.post(reverse('inventario:movimiento'), data)
        self.assertEqual(r.status_code, 302)
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock_actual, stock_inicial - 20)

    def test_movimiento_ajuste_fija_stock(self):
        self.client.force_login(self.u)
        data = {'producto': self.prod.pk, 'tipo': 'ajuste',
                'cantidad': '75', 'motivo': 'Inventario físico'}
        r = self.client.post(reverse('inventario:movimiento'), data)
        self.assertEqual(r.status_code, 302)
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock_actual, 75)

    def test_proveedores(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('inventario:proveedores'))
        self.assertEqual(r.status_code, 200)

    def test_crear_proveedor_post(self):
        self.client.force_login(self.u)
        data = {'nombre': 'Pharma SA', 'ruc': '80012345-6',
                'telefono': '021123456', 'email': '', 'direccion': '',
                'contacto': '', 'activo': True}
        r = self.client.post(reverse('inventario:crear_proveedor'), data)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Proveedor.objects.filter(nombre='Pharma SA').exists())
