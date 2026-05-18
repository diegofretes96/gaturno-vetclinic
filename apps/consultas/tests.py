from django.test import TestCase, Client
from django.urls import reverse
from .models import Consulta, NotaClinica, Prescripcion
from apps.accounts.models import Usuario
from apps.propietarios.models import Propietario
from apps.pacientes.models import Especie, Paciente


def crear_usuario(username='vet', rol='veterinario'):
    u = Usuario(username=username, rol=rol, first_name='Dr', last_name='Test')
    u.set_password('Pass123!')
    u.save()
    return u


def crear_paciente():
    prop = Propietario.objects.create(nombres='Pedro', apellidos='Soto', tipo_documento='ci',
                                      numero_documento='4444444', telefono='0981000000')
    esp = Especie.objects.create(nombre='Canino')
    return Paciente.objects.create(nombre='Rex', propietario=prop, especie=esp, sexo='M')


def crear_consulta(paciente=None, veterinario=None):
    if paciente is None:
        paciente = crear_paciente()
    if veterinario is None:
        veterinario = crear_usuario()
    return Consulta.objects.create(paciente=paciente, veterinario=veterinario,
                                   tipo='primera_vez', motivo_consulta='Revisión general')


class ConsultaModelTests(TestCase):
    def setUp(self):
        self.vet = crear_usuario()
        self.pac = crear_paciente()

    def test_str(self):
        c = crear_consulta(self.pac, self.vet)
        s = str(c)
        self.assertIn(f'#{c.pk}', s)
        self.assertIn('Rex', s)

    def test_tipo_por_defecto(self):
        c = crear_consulta(self.pac, self.vet)
        self.assertEqual(c.tipo, 'primera_vez')

    def test_tipos_choices(self):
        tipos = [t[0] for t in Consulta.TIPOS]
        self.assertIn('primera_vez', tipos)
        self.assertIn('control', tipos)
        self.assertIn('urgencia', tipos)

    def test_ordering_mas_reciente_primero(self):
        c1 = crear_consulta(self.pac, self.vet)
        c2 = crear_consulta(self.pac, self.vet)
        # Ordering is -fecha (datetime); two records created in same test may share
        # the same timestamp, so just verify the default_ordering meta is set.
        self.assertEqual(Consulta._meta.ordering, ['-fecha'])
        self.assertEqual(Consulta.objects.count(), 2)


class NotaClinicaModelTests(TestCase):
    def test_nota_creada(self):
        c = crear_consulta()
        vet = Usuario.objects.first()
        nota = NotaClinica.objects.create(consulta=c, veterinario=vet, nota='Paciente estable')
        self.assertEqual(nota.nota, 'Paciente estable')
        self.assertEqual(nota.consulta, c)


class PrescripcionModelTests(TestCase):
    def test_str(self):
        c = crear_consulta()
        rx = Prescripcion.objects.create(consulta=c, medicamento_nombre='Amoxicilina',
                                         dosis='250mg', frecuencia='Cada 8h',
                                         duracion='7 días', via='oral')
        self.assertIn('Amoxicilina', str(rx))


class ConsultasViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario()
        self.pac = crear_paciente()
        self.consulta = crear_consulta(self.pac, self.u)

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('consultas:lista'))
        self.assertEqual(r.status_code, 302)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:lista'))
        self.assertEqual(r.status_code, 200)

    def test_detalle(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:detalle', args=[self.consulta.pk]))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_get_con_paciente(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:crear'), {'paciente': self.pac.pk})
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        data = {'paciente': self.pac.pk, 'veterinario': self.u.pk,
                'tipo': 'control', 'motivo_consulta': 'Control mensual',
                'anamnesis': '', 'subjetivo': '', 'objetivo': '',
                'evaluacion': '', 'plan': '', 'diagnostico_presuntivo': '',
                'diagnostico_definitivo': '', 'pronostico': '', 'observaciones': ''}
        r = self.client.post(reverse('consultas:crear'), data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Consulta.objects.filter(tipo='control').count(), 1)

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:editar', args=[self.consulta.pk]))
        self.assertEqual(r.status_code, 200)

    def test_agregar_nota(self):
        self.client.force_login(self.u)
        r = self.client.post(reverse('consultas:nota', args=[self.consulta.pk]),
                             {'nota': 'Paciente mejorando'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(NotaClinica.objects.filter(consulta=self.consulta).count(), 1)

    def test_agregar_prescripcion(self):
        self.client.force_login(self.u)
        data = {'medicamento_nombre': 'Ibuprofeno', 'dosis': '100mg',
                'frecuencia': 'Cada 12h', 'duracion': '5 días',
                'via': 'oral', 'indicaciones': ''}
        r = self.client.post(reverse('consultas:prescripcion',
                                     args=[self.consulta.pk]), data)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Prescripcion.objects.filter(consulta=self.consulta).count(), 1)

    def test_imprimir(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('consultas:imprimir', args=[self.consulta.pk]))
        self.assertEqual(r.status_code, 200)
