from django.test import TestCase, Client
from django.urls import reverse
from .models import Usuario


def crear_usuario(**kwargs):
    defaults = dict(username='testuser', password='TestPass123!', rol='veterinario',
                    first_name='Test', last_name='User')
    defaults.update(kwargs)
    password = defaults.pop('password')
    u = Usuario(**defaults)
    u.set_password(password)
    u.save()
    return u


class UsuarioModelTests(TestCase):
    def test_str_con_nombre(self):
        u = crear_usuario(first_name='Ana', last_name='García', rol='veterinario')
        self.assertIn('Ana García', str(u))
        self.assertIn('Veterinario', str(u))

    def test_str_sin_nombre(self):
        u = crear_usuario(first_name='', last_name='', username='jdoe', rol='admin')
        self.assertIn('jdoe', str(u))

    def test_nombre_completo_con_nombre(self):
        u = crear_usuario(first_name='Ana', last_name='García')
        self.assertEqual(u.nombre_completo, 'Ana García')

    def test_nombre_completo_sin_nombre(self):
        u = crear_usuario(first_name='', last_name='', username='jdoe')
        self.assertEqual(u.nombre_completo, 'jdoe')

    def test_es_veterinario_veterinario(self):
        u = crear_usuario(rol='veterinario')
        self.assertTrue(u.es_veterinario)

    def test_es_veterinario_admin(self):
        u = crear_usuario(username='admin2', rol='admin')
        self.assertTrue(u.es_veterinario)

    def test_es_veterinario_recepcionista(self):
        u = crear_usuario(rol='recepcionista')
        self.assertFalse(u.es_veterinario)

    def test_iniciales_con_nombre(self):
        u = crear_usuario(first_name='Ana', last_name='García')
        self.assertEqual(u.iniciales, 'AG')

    def test_iniciales_sin_nombre(self):
        u = crear_usuario(first_name='', last_name='', username='jdoe')
        self.assertEqual(u.iniciales, 'JD')

    def test_roles_choices(self):
        roles = [r[0] for r in Usuario.ROLES]
        self.assertIn('admin', roles)
        self.assertIn('veterinario', roles)
        self.assertIn('asistente', roles)
        self.assertIn('recepcionista', roles)
        self.assertIn('esteticista', roles)


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario(username='doc', password='DocPass123!')
        self.url = reverse('accounts:login')

    def test_get_login_page(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'form')

    def test_login_credenciales_correctas(self):
        r = self.client.post(self.url, {'username': 'doc', 'password': 'DocPass123!'})
        self.assertIn(r.status_code, [200, 302])

    def test_login_credenciales_incorrectas(self):
        r = self.client.post(self.url, {'username': 'doc', 'password': 'wrong'})
        self.assertEqual(r.status_code, 200)

    def test_usuario_autenticado_redirigido(self):
        self.client.force_login(self.u)
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 302)


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.u = crear_usuario(username='admin_u', password='Pass123!', rol='admin',
                               first_name='Admin', last_name='User')

    def test_lista_requiere_login(self):
        r = self.client.get(reverse('accounts:lista'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login', r.url)

    def test_lista_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('accounts:lista'))
        self.assertEqual(r.status_code, 200)

    def test_perfil_autenticado(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('accounts:perfil'))
        self.assertEqual(r.status_code, 200)

    def test_crear_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('accounts:crear'))
        self.assertEqual(r.status_code, 200)

    def test_crear_post_valido(self):
        self.client.force_login(self.u)
        data = {'username': 'nuevo_vet', 'password1': 'VetPass456!', 'password2': 'VetPass456!',
                'first_name': 'Nuevo', 'last_name': 'Vet', 'rol': 'veterinario', 'email': ''}
        r = self.client.post(reverse('accounts:crear'), data)
        self.assertIn(r.status_code, [200, 302])

    def test_editar_get(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('accounts:editar', args=[self.u.pk]))
        self.assertEqual(r.status_code, 200)

    def test_logout_redirige(self):
        self.client.force_login(self.u)
        r = self.client.get(reverse('accounts:logout'))
        self.assertEqual(r.status_code, 302)
