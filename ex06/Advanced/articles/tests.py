# In articles/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Favourite
from django.utils import timezone

from django.utils import translation

class FavouritesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.article = Article.objects.create(
            title='Test Article',
            synopsis='Test Synopsis',
            author=self.user,
            published_date=timezone.now()
        )
        # Establecer el idioma predeterminado para las pruebas
        translation.activate('en')

    def tearDown(self):
        translation.deactivate()

    def test_favourites_view_access(self):
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200, "El usuario autenticado debería tener acceso a la vista de favoritos.")
        self.client.logout()
        response = self.client.get(reverse('favourites'))
        self.assertNotEqual(response.status_code, 200)


class RegisterViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_registered_user_cannot_access_register_form(self):
        # Usuario autenticado no debería poder acceder al formulario de registro
        response = self.client.get(reverse('register'))
        self.assertNotEqual(response.status_code, 200, "El usuario autenticado no debería poder acceder al formulario de registro.")
        
        # Después de cerrar sesión, debería poder acceder al formulario
        self.client.logout()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

