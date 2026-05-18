import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import Vacuna, Vacunacion
from apps.accounts.models import Usuario
from apps.propietarios.models import Propietario
from apps.pacientes.models import Especie, Paciente


def crear_usuario():
    u = Usuario(username='vet', rol='veterinario', first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_especie(nombre='Canino'):
    return Especie.objects.create(nombre=nombre)


def crear_paciente(especie=None):
    if especie is None:
        especie = crear_especie()
    prop = Propietario.objects.create(nombres='Luis', apellidos='Mora', tipo_documento='ci',
                                      numero_documento='3333333', telefono='0981000000')
    return Paciente.objects.create(nombre='Toby', propietario=prop, especie=especie, sexo='M')


def crear_vacuna(especie=None, intervalo=365):
    if especie is None:
        especie = crear_especie()
    return Vacuna.objects.create(nombre='Antirrábica', especie=especie,
                                 intervalo_dias=intervalo)


class VacunaModelTests(TestCase):
    def test_str(self):
        e = crear_especie()
        v = crear_vacuna(e)
        self.assertIn('Antirrábica', str(v))
        self.assertIn('Canino', str(v))

    def test_activo_por_defecto(self):
        v = crear_vacuna()
        self.assertTrue(v.activo)

    def test_intervalo_defecto(self):
        v = crear_vacuna()
        self.assertEqual(v.intervalo_dias, 365)


class VacunacionModelTests(TestCase):
    def setUp(self):
        self.u = crear_usuario()
        self.esp = crear_especie()
        self.pac = crear_paciente(self.esp)
        self.vac = crear_vacuna(self.esp, intervalo=365)

    def test_str(self):
        hoy = datetime.date.today()
        v = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                      veterinario=self.u, fecha_aplicacion=hoy)
        s = str(v)
        self.assertIn('Antirrábica', s)
        self.assertIn('Toby', s)

    def test_proxima_dosis_calculada_automaticamente(self):
        hoy = datetime.date.today()
        v = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                      veterinario=self.u, fecha_aplicacion=hoy)
        expected = hoy + datetime.timedelta(days=365)
        self.assertEqual(v.proxima_dosis, expected)

    def test_proxima_dosis_no_sobreescribe_si_ya_existe(self):
        hoy = datetime.date.today()
        proxima_manual = hoy + datetime.timedelta(days=180)
        v = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                      veterinario=self.u, fecha_aplicacion=hoy,
                                      proxima_dosis=proxima_manual)
        self.assertEqual(v.proxima_dosis, proxima_manual)

    def test_proxima_dosis_intervalo_diferente(self):
        vac_semestral = Vacuna.objects.create(nombre='Sextuple', especie=self.esp,
                                             intervalo_dias=180)
        hoy = datetime.date.today()
        v = Vacunacion.objects.create(paciente=self.pac, vacuna=vac_semestral,
                                      veterinario=self.u, fecha_aplicacion=hoy)
        expected = hoy + datetime.timedelta(days=180)
        self.assertEqual(v.proxima_dosis, expected)

    def test_ordering_mas_reciente_primero(self):
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)
        v1 = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                       veterinario=self.u, fecha_aplicacion=ayer)
        v2 = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                       veterinario=self.u, fecha_aplicacion=hoy)
        qs = list(Vacunacion.objects.all())
        self.assertEqual(qs[0].pk, v2.pk)


class VacunacionViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.esp = crear_especie()
        self.pac = crear_paciente(self.esp)
        self.vac = crear_vacuna(self.esp)
        hoy = datetime.date.today()
        self.registro = Vacunacion.objects.create(paciente=self.pac, vacuna=self.vac,
                                                  veterinario=self.u, fecha_aplicacion=hoy)

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('vacunacion:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('vacunacion:lista'))
        self.assertEqual(r.status_code, 200)

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('vacunacion:detalle', args=[self.registro.pk]))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('vacunacion:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        data = {'paciente': self.pac.pk, 'vacuna': self.vac.pk,
                'veterinario': self.u.pk,
                'fecha_aplicacion': datetime.date.today().isoformat(),
                'lote': 'L001', 'dosis': '1ml', 'via': 'SC',
                'sitio': 'cuello', 'observaciones': ''}
        r = self.client.post(reverse('vacunacion:crear'), data)
        self.assertEqual(r.status_code, 302)

    def test_catalogo_vacunas(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('vacunacion:vacunas'))
        self.assertEqual(r.status_code, 200)
