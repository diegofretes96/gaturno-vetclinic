from django.test import TestCase, Client
from django.urls import reverse
from .models import Factura, ItemFactura
from apps.accounts.models import Usuario
from apps.propietarios.models import Propietario
from apps.pacientes.models import Especie, Paciente


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_propietario():
    return Propietario.objects.create(nombres='Ana', apellidos='Castro', tipo_documento='ci',
                                      numero_documento='7777777', telefono='0981000000')


def crear_paciente(propietario=None):
    if propietario is None:
        propietario = crear_propietario()
    esp = Especie.objects.create(nombre='Canino')
    return Paciente.objects.create(nombre='Perla', propietario=propietario, especie=esp, sexo='H')


def crear_factura(propietario=None, usuario=None):
    if propietario is None:
        propietario = crear_propietario()
    if usuario is None:
        usuario = crear_usuario()
    return Factura.objects.create(propietario=propietario, creado_por=usuario)


class FacturaModelTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.prop = crear_propietario()

    def test_str(self):
        f = crear_factura(self.prop, self.u)
        s = str(f)
        self.assertIn('Factura #', s)
        self.assertIn('Castro', s)

    def test_numero_generado_automaticamente(self):
        f = crear_factura(self.prop, self.u)
        self.assertTrue(f.numero.startswith('F'))
        self.assertEqual(len(f.numero), 7)

    def test_numeros_unicos(self):
        f1 = crear_factura(self.prop, self.u)
        f2 = crear_factura(self.prop, self.u)
        self.assertNotEqual(f1.numero, f2.numero)

    def test_estado_por_defecto(self):
        f = crear_factura(self.prop, self.u)
        self.assertEqual(f.estado, 'borrador')

    def test_saldo_pendiente_sin_pago(self):
        f = crear_factura(self.prop, self.u)
        f.total = 100000
        f.save()
        self.assertEqual(f.saldo_pendiente, 100000)

    def test_saldo_pendiente_con_pago_parcial(self):
        f = crear_factura(self.prop, self.u)
        f.total = 100000
        f.monto_pagado = 40000
        f.save()
        self.assertEqual(f.saldo_pendiente, 60000)

    def test_estados_choices(self):
        estados = [e[0] for e in Factura.ESTADOS]
        self.assertIn('borrador', estados)
        self.assertIn('emitida', estados)
        self.assertIn('pagada', estados)
        self.assertIn('anulada', estados)

    def test_metodos_pago_choices(self):
        metodos = [m[0] for m in Factura.METODOS]
        self.assertIn('efectivo', metodos)
        self.assertIn('tarjeta_credito', metodos)
        self.assertIn('transferencia', metodos)


class ItemFacturaModelTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.prop = crear_propietario()
        self.f = crear_factura(self.prop, self.u)

    def test_str(self):
        item = ItemFactura.objects.create(factura=self.f, descripcion='Consulta',
                                          cantidad=1, precio_unitario=50000)
        self.assertIn('Consulta', str(item))
        self.assertIn('x1', str(item))

    def test_subtotal_calculado_automaticamente(self):
        item = ItemFactura.objects.create(factura=self.f, descripcion='Consulta',
                                          cantidad=2, precio_unitario=30000,
                                          descuento_item=5000)
        self.assertEqual(item.subtotal, 55000)

    def test_subtotal_sin_descuento(self):
        item = ItemFactura.objects.create(factura=self.f, descripcion='Vacuna',
                                          cantidad=1, precio_unitario=40000)
        self.assertEqual(item.subtotal, 40000)


class FacturaCalcTotalesTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.prop = crear_propietario()
        self.f = crear_factura(self.prop, self.u)

    def test_calcular_totales_un_item(self):
        ItemFactura.objects.create(factura=self.f, descripcion='Consulta',
                                   cantidad=1, precio_unitario=100000)
        self.f.calcular_totales()
        self.f.refresh_from_db()
        self.assertEqual(self.f.subtotal, 100000)
        self.assertEqual(self.f.iva, 10000)
        self.assertEqual(self.f.total, 110000)

    def test_calcular_totales_multiples_items(self):
        ItemFactura.objects.create(factura=self.f, descripcion='Item A',
                                   cantidad=2, precio_unitario=50000)
        ItemFactura.objects.create(factura=self.f, descripcion='Item B',
                                   cantidad=1, precio_unitario=20000)
        self.f.calcular_totales()
        self.f.refresh_from_db()
        self.assertEqual(self.f.subtotal, 120000)

    def test_calcular_totales_sin_items(self):
        self.f.calcular_totales()
        self.f.refresh_from_db()
        self.assertEqual(self.f.subtotal, 0)
        self.assertEqual(self.f.total, 0)


class FacturacionViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.prop = crear_propietario()
        self.pac = crear_paciente(self.prop)
        self.f = crear_factura(self.prop, self.u)

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('facturacion:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_filtro_estado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:lista'), {'estado': 'borrador'})
        self.assertEqual(r.status_code, 200)

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:detalle', args=[self.f.pk]))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        from django.utils import timezone
        self.client.force_login(self.u)
        fecha = timezone.now().strftime('%Y-%m-%dT%H:%M')
        data = {'propietario': self.prop.pk, 'estado': 'borrador',
                'fecha_emision': fecha,
                'metodo_pago': '', 'descuento': '0', 'observaciones': ''}
        r = self.client.post(reverse('facturacion:crear'), data)
        self.assertEqual(r.status_code, 302)

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:editar', args=[self.f.pk]))
        self.assertEqual(r.status_code, 200)

    def test_agregar_item_post(self):
        self.client.force_login(self.u)
        data = {'descripcion': 'Consulta médica', 'cantidad': '1',
                'precio_unitario': '80000', 'descuento_item': '0'}
        r = self.client.post(reverse('facturacion:agregar_item', args=[self.f.pk]), data)
        self.assertEqual(r.status_code, 302)
        self.f.refresh_from_db()
        self.assertGreater(self.f.subtotal, 0)

    def test_cobrar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:cobrar', args=[self.f.pk]))
        self.assertEqual(r.status_code, 200)

    def test_cobrar_post_marca_pagada(self):
        self.client.force_login(self.u)
        self.f.total = 50000
        self.f.save()
        r = self.client.post(reverse('facturacion:cobrar', args=[self.f.pk]),
                             {'metodo_pago': 'efectivo'})
        self.assertEqual(r.status_code, 302)
        self.f.refresh_from_db()
        self.assertEqual(self.f.estado, 'pagada')
        self.assertEqual(self.f.metodo_pago, 'efectivo')

    def test_imprimir(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('facturacion:imprimir', args=[self.f.pk]))
        self.assertEqual(r.status_code, 200)

    def test_eliminar_item(self):
        self.client.force_login(self.u)
        item = ItemFactura.objects.create(factura=self.f, descripcion='Test',
                                          cantidad=1, precio_unitario=10000)
        r = self.client.post(reverse('facturacion:eliminar_item',
                                     args=[self.f.pk, item.pk]))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(ItemFactura.objects.filter(pk=item.pk).exists())
