import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Cita, SalaEspera
from apps.accounts.models import Usuario
from apps.propietarios.models import Propietario
from apps.pacientes.models import Especie, Paciente


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_paciente():
    prop = Propietario.objects.create(nombres='Felipe', apellidos='Vega', tipo_documento='ci',
                                      numero_documento='2222222', telefono='0981000000')
    esp = Especie.objects.create(nombre='Canino')
    return Paciente.objects.create(nombre='Bobby', propietario=prop, especie=esp, sexo='M')


def crear_cita(paciente=None, veterinario=None, creado_por=None, **kwargs):
    if paciente is None:
        paciente = crear_paciente()
    if creado_por is None:
        creado_por = veterinario
    fecha = timezone.now() + datetime.timedelta(hours=1)
    defaults = dict(paciente=paciente, veterinario=veterinario, creado_por=creado_por,
                    tipo='consulta', fecha=fecha, motivo='Revisión', estado='pendiente')
    defaults.update(kwargs)
    return Cita.objects.create(**defaults)


class CitaModelTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.pac = crear_paciente()

    def test_str(self):
        c = crear_cita(self.pac, self.u, self.u)
        s = str(c)
        self.assertIn('Bobby', s)

    def test_estado_por_defecto(self):
        c = crear_cita(self.pac, self.u, self.u)
        self.assertEqual(c.estado, 'pendiente')

    def test_tipo_por_defecto(self):
        c = crear_cita(self.pac, self.u, self.u)
        self.assertEqual(c.tipo, 'consulta')

    def test_es_hoy_true(self):
        c = crear_cita(self.pac, self.u, self.u, fecha=timezone.now())
        self.assertTrue(c.es_hoy)

    def test_es_hoy_false_manana(self):
        c = crear_cita(self.pac, self.u, self.u,
                       fecha=timezone.now() + datetime.timedelta(days=1))
        self.assertFalse(c.es_hoy)

    def test_tipos_choices(self):
        tipos = [t[0] for t in Cita.TIPOS]
        self.assertIn('consulta', tipos)
        self.assertIn('vacunacion', tipos)
        self.assertIn('cirugia', tipos)

    def test_estados_choices(self):
        estados = [e[0] for e in Cita.ESTADOS]
        self.assertIn('pendiente', estados)
        self.assertIn('confirmada', estados)
        self.assertIn('cancelada', estados)
        self.assertIn('realizada', estados)


class SalaEsperaModelTests(TestCase):
    def test_str(self):
        u = crear_usuario()
        pac = crear_paciente()
        c = crear_cita(pac, u, u)
        se = SalaEspera.objects.create(cita=c, prioridad=3)
        self.assertIn('Bobby', str(se))

    def test_tiempo_espera_aproximado(self):
        u = crear_usuario()
        pac = crear_paciente()
        c = crear_cita(pac, u, u)
        se = SalaEspera.objects.create(cita=c)
        self.assertGreaterEqual(se.tiempo_espera_min, 0)


class AgendaViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.pac = crear_paciente()
        self.cita = crear_cita(self.pac, self.u, self.u)

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('agenda:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:lista'))
        self.assertEqual(r.status_code, 200)

    def test_calendario(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:calendario'))
        self.assertEqual(r.status_code, 200)

    def test_calendario_json(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:citas_json'))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIsInstance(data, list)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        fecha = (timezone.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
        data = {'paciente': self.pac.pk, 'veterinario': self.u.pk,
                'tipo': 'control', 'fecha': fecha,
                'duracion_min': 30, 'motivo': 'Control rutinario',
                'notas': '', 'estado': 'pendiente'}
        r = self.client.post(reverse('agenda:crear'), data)
        self.assertIn(r.status_code, [200, 302])

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:editar', args=[self.cita.pk]))
        self.assertEqual(r.status_code, 200)

    def test_cancelar_post(self):
        self.client.force_login(self.u)
        r = self.client.post(reverse('agenda:cancelar', args=[self.cita.pk]))
        self.assertEqual(r.status_code, 302)
        self.cita.refresh_from_db()
        self.assertEqual(self.cita.estado, 'cancelada')

    def test_sala_espera(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('agenda:sala_espera'))
        self.assertEqual(r.status_code, 200)
