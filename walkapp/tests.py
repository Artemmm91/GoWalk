from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class RecoverPassPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('recover_password')

    def test_page_downloaded(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'billy_the_messenger/recover_password.html')


class UserProfilePage(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('userprofile')

    def test_page_downloaded(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TestSignInPage(TestCase):

    def setUp(self):
        u = User(username="testuser", first_name="Vasya", last_name="Pupkin", is_active=1)
        u.set_password('pass')
        u.save()
        self.client = Client()
        self.url = reverse("signin")

    def test_signin_page_downloaded(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_signin_page_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'billy_the_messenger/signin.html')

    def test_signin_page_wrong_data(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'passh'})
        f = AuthenticationForm(data=response.wsgi_request.POST)
        f.is_valid()
        array = f.errors['__all__']
        flag = False
        for i in range(len(array)):
            if array[i] == 'Пожалуйста, введите правильные имя пользователя и пароль. ' \
                           'Оба поля могут быть чувствительны к регистру.':
                flag = True
        self.assertTrue(flag)

    def test_signin_page_required_password(self):
        response = self.client.post(self.url, {'username': 'testuser', 'passwor': 'passh'})
        f = AuthenticationForm(data=response.wsgi_request.POST)
        f.is_valid()
        array = f.errors['password']
        flag = False
        for i in range(len(array)):
            if array[i] == 'Обязательное поле.':
                flag = True
        self.assertTrue(flag)

    def test_signin_page_required_username(self):
        response = self.client.post(self.url, {'username': 'testuse', 'password': 'pass'})
        f = AuthenticationForm(data=response.wsgi_request.POST)
        f.is_valid()
        array = f.errors['username']
        flag = False
        for i in range(len(array)):
            if array[i] == 'Обязательное поле.':
                flag = True
        self.assertTrue(flag)

    def test_signin_page_empty_fields(self):
        response1 = self.client.post(self.url, {'username': 'testing_user', 'password': ''})
        response2 = self.client.post(self.url, {'username': '', 'password': 'pass'})
        f1 = AuthenticationForm(data=response1.wsgi_request.POST)
        f2 = AuthenticationForm(data=response2.wsgi_request.POST)
        f1.is_valid()
        f2.is_valid()
        array1 = f1.errors['password']
        array2 = f2.errors['username']
        flag1 = False
        for i in range(len(array1)):
            if array1[i] == 'Обязательное поле.':
                flag1 = True
        flag2 = False
        for i in range(len(array2)):
            if array2[i] == 'Обязательное поле.':
                flag2 = True
        self.assertTrue(flag1)
        self.assertTrue(flag2)

    def test_signin_page_ok(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'pass'})
        f = AuthenticationForm(data=response.wsgi_request.POST)
        f.is_valid()
        dic = f.errors
        flag = False
        if len(dic) == 0:
            flag = True
        self.assertTrue(flag)
