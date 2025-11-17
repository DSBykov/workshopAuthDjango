from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AuthTests(TestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view_get(self):
        """Проверка GET-запроса к странице входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_view_post_valid(self):
        """Проверка успешного входа с правильными данными"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_post_invalid(self):
        """Проверка входа с неверным паролем"""
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        form = response.context['form']
        self.assertIn(
            member='Пожалуйста, введите правильные имя пользователя и пароль. '
                   'Оба поля могут быть чувствительны к регистру.',
            container=form.non_field_errors()
        )

    def test_signin_view_get(self):
        """Проверка GET-запроса к форме регистрации"""
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_signin_view_post_valid(self):
        """Проверка успешной регистрации нового пользователя"""
        data = {
            'username': 'newuser',
            'password1': 'newpass456',
            'password2': 'newpass456'
        }
        response = self.client.post(reverse('signin'), data)
        self.assertRedirects(response, reverse('home'))

        # Проверяем, что пользователь создан
        user = User.objects.get(username=data['username'])
        self.assertTrue(
            user.check_password(data['password1']),
            msg='Пароль нового пользователя не совпадает'
        )

        self.assertTrue(
            self.client.session.get('_auth_user_id'),
            msg='Не выполняется автоматическая авторизация нового пользователя.'
        )

        self.assertEqual(
            first=int(self.client.session.get('_auth_user_id')),
            second=user.pk,
            msg='Авторизация выполнена под другим пользователем'
        )

    def test_signin_view_post_password_mismatch(self):
        """Проверка ошибки при несовпадении паролей"""
        data = {
            'username': 'newuser',
            'password1': 'pass1',
            'password2': 'pass2',  # не совпадает
        }
        response = self.client.post(reverse('signin'), data)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form,
            field='password2',
            errors='Введенные пароли не совпадают.',
        )

    def test_logout_confirm_view(self):
        """Проверка страницы подтверждения выхода"""
        response = self.client.get(reverse('logout-confirm'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')
