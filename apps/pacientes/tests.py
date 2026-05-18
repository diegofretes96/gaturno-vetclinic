import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Especie, Raza, Paciente
from apps.propietarios.models import Propietario
from apps.accounts.models import Usuario


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_propietario():
    return Propietario.objects.create(nombres='Carlos', apellidos='Ruiz',
                                      tipo_documento='ci', numero_documento='5555555',
                                      telefono='0981000000')


def crear_especie(nombre='Canino'):
    return Especie.objects.create(nombre=nombre)


def crear_raza(especie, nombre='Labrador'):
    return Raza.objects.create(especie=especie, nombre=nombre)


def crear_paciente(propietario=None, especie=None, **kwargs):
    if propietario is None:
        propietario = crear_propietario()
    if especie is None:
        especie = crear_especie()
    defaults = dict(nombre='Max', sexo='M', propietario=propietario, especie=especie)
    defaults.update(kwargs)
    return Paciente.objects.create(**defaults)


class EspecieModelTests(TestCase):
    def test_str(self):
        e = crear_especie('Felino')
        self.assertEqual(str(e), 'Felino')

    def test_unico(self):
        crear_especie('Canino')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            crear_especie('Canino')


class RazaModelTests(TestCase):
    def test_str(self):
        e = crear_especie()
        r = crear_raza(e, 'Poodle')
        self.assertEqual(str(r), 'Poodle')

    def test_unico_por_especie(self):
        e = crear_especie()
        crear_raza(e, 'Labrador')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            crear_raza(e, 'Labrador')


class PacienteModelTests(TestCase):
    def setUp(self):
        self.esp = crear_especie('Canino')
        self.prop = crear_propietario()

    def test_str(self):
        p = crear_paciente(propietario=self.prop, especie=self.esp, nombre='Rex')
        self.assertIn('Rex', str(p))
        self.assertIn('Ruiz', str(p))

    def test_estado_activo_por_defecto(self):
        p = crear_paciente(propietario=self.prop, especie=self.esp)
        self.assertEqual(p.estado, 'activo')

    def test_no_esterilizado_por_defecto(self):
        p = crear_paciente(propietario=self.prop, especie=self.esp)
        self.assertFalse(p.esterilizado)

    def test_edad_desconocida_sin_fecha(self):
        p = crear_paciente(propietario=self.prop, especie=self.esp)
        self.assertEqual(p.edad, 'Desconocida')

    def test_edad_con_fecha(self):
        fn = timezone.now().date() - datetime.timedelta(days=365 * 2 + 30)
        p = crear_paciente(propietario=self.prop, especie=self.esp, fecha_nacimiento=fn)
        self.assertIn('a', p.edad)

    def test_edad_meses(self):
        fn = timezone.now().date() - datetime.timedelta(days=60)
        p = crear_paciente(propietario=self.prop, especie=self.esp, fecha_nacimiento=fn)
        self.assertIn('mes', p.edad)

    def test_emoji_canino(self):
        p = crear_paciente(propietario=self.prop, especie=self.esp)
        self.assertEqual(p.emoji, '🐶')

    def test_emoji_felino(self):
        esp_gat = crear_especie('Gatuno')
        p = crear_paciente(propietario=self.prop, especie=esp_gat)
        self.assertEqual(p.emoji, '😺')

    def test_microchip_unico(self):
        crear_paciente(propietario=self.prop, especie=self.esp, microchip='MC001')
        from django.db import IntegrityError
        prop2 = Propietario.objects.create(nombres='Otro', apellidos='Otro',
                                           tipo_documento='ci', numero_documento='8888888',
                                           telefono='0982000000')
        with self.assertRaises(IntegrityError):
            crear_paciente(propietario=prop2, especie=self.esp,
                           nombre='Otro', microchip='MC001')


class PacientesViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.esp = crear_especie()
        self.prop = crear_propietario()
        self.pac = crear_paciente(propietario=self.prop, especie=self.esp)

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_filtro_especie(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:lista'), {'especie': self.esp.pk})
        self.assertEqual(r.status_code, 200)

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:detalle', args=[self.pac.pk]))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_con_propietario_inicial(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:crear'), {'propietario': self.prop.pk})
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        data = {'nombre': 'Luna', 'propietario': self.prop.pk, 'especie': self.esp.pk,
                'sexo': 'H', 'estado': 'activo', 'color': '', 'alergias': '',
                'antecedentes': '', 'esterilizado': False}
        r = self.client.post(reverse('pacientes:crear'), data)
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Paciente.objects.filter(nombre='Luna').exists())

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('pacientes:editar', args=[self.pac.pk]))
        self.assertEqual(r.status_code, 200)

    def test_eliminar_post_da_de_baja(self):
        self.client.force_login(self.u)
        r = self.client.post(reverse('pacientes:eliminar', args=[self.pac.pk]))
        self.assertEqual(r.status_code, 302)
        self.pac.refresh_from_db()
        self.assertEqual(self.pac.estado, 'dado_baja')

    def test_razas_ajax(self):
        raza = crear_raza(self.esp)
        r = self.client.get(reverse('pacientes:razas'), {'especie_id': self.esp.pk})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('razas', data)
        self.assertEqual(len(data['razas']), 1)

    def test_buscar_ajax(self):
        r = self.client.get(reverse('pacientes:buscar'), {'q': 'Max'})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('results', data)
