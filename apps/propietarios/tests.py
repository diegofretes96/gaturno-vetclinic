from django.test import TestCase, Client
from django.urls import reverse
from .models import Propietario
from apps.accounts.models import Usuario


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_propietario(**kwargs):
    defaults = dict(nombres='Juan', apellidos='Pérez', tipo_documento='ci',
                    numero_documento='1234567', telefono='0981123456')
    defaults.update(kwargs)
    return Propietario.objects.create(**defaults)


class PropietarioModelTests(TestCase):
    def test_str(self):
        p = crear_propietario()
        self.assertEqual(str(p), 'Pérez, Juan')

    def test_nombre_completo(self):
        p = crear_propietario()
        self.assertEqual(p.nombre_completo, 'Juan Pérez')

    def test_total_mascotas_sin_mascotas(self):
        p = crear_propietario()
        self.assertEqual(p.total_mascotas, 0)

    def test_activo_por_defecto(self):
        p = crear_propietario()
        self.assertTrue(p.activo)

    def test_tipo_documento_choices(self):
        tipos = [t[0] for t in Propietario.TIPO_DOC]
        self.assertIn('ci', tipos)
        self.assertIn('ruc', tipos)
        self.assertIn('pasaporte', tipos)

    def test_numero_documento_unico(self):
        crear_propietario(numero_documento='9999999')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            crear_propietario(nombres='Otro', apellidos='Otro', numero_documento='9999999')

    def test_ordering_apellidos(self):
        crear_propietario(nombres='Carlos', apellidos='Zamora', numero_documento='111')
        crear_propietario(nombres='Ana', apellidos='Alves', numero_documento='222')
        qs = list(Propietario.objects.all())
        self.assertEqual(qs[0].apellidos, 'Alves')


class PropietariosViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.p = crear_propietario()

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('propietarios:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_busqueda(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:lista'), {'q': 'Pérez'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Pérez')

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:detalle', args=[self.p.pk]))
        self.assertEqual(r.status_code, 200)

    def test_detalle_no_existe(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:detalle', args=[99999]))
        self.assertEqual(r.status_code, 404)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        data = {'nombres': 'María', 'apellidos': 'López', 'tipo_documento': 'ci',
                'numero_documento': '7654321', 'telefono': '0982000000',
                'telefono_alt': '', 'email': '', 'direccion': '', 'ciudad': '',
                'observaciones': ''}
        r = self.client.post(reverse('propietarios:crear'), data)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Propietario.objects.filter(numero_documento='7654321').exists())

    def test_crear_post_doc_duplicado(self):
        self.client.force_login(self.u)
        data = {'nombres': 'Otro', 'apellidos': 'Otro', 'tipo_documento': 'ci',
                'numero_documento': '1234567', 'telefono': '0000000000',
                'telefono_alt': '', 'email': '', 'direccion': '', 'ciudad': '',
                'observaciones': ''}
        r = self.client.post(reverse('propietarios:crear'), data)
        self.assertEqual(r.status_code, 200)

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:editar', args=[self.p.pk]))
        self.assertEqual(r.status_code, 200)

    def test_editar_post(self):
        self.client.force_login(self.u)
        data = {'nombres': 'Juan Updated', 'apellidos': 'Pérez', 'tipo_documento': 'ci',
                'numero_documento': '1234567', 'telefono': '0981999999',
                'telefono_alt': '', 'email': '', 'direccion': '', 'ciudad': '',
                'observaciones': ''}
        r = self.client.post(reverse('propietarios:editar', args=[self.p.pk]), data)
        self.assertEqual(r.status_code, 302)
        self.p.refresh_from_db()
        self.assertEqual(self.p.nombres, 'Juan Updated')

    def test_eliminar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('propietarios:eliminar', args=[self.p.pk]))
        self.assertEqual(r.status_code, 200)

    def test_eliminar_post_desactiva(self):
        self.client.force_login(self.u)
        r = self.client.post(reverse('propietarios:eliminar', args=[self.p.pk]))
        self.assertEqual(r.status_code, 302)
        self.p.refresh_from_db()
        self.assertFalse(self.p.activo)
