from django.test import TestCase
from django.contrib.auth import get_user_model

class UsuarioModelTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        # Teste a criação de um usuário
        user = self.user_model.objects.create_user(username='testuser',first_name='Usuario teste',cpf='000.000.000-00',password='testpass123')
        self.assertIsInstance(user, self.user_model)
        self.assertEqual(user.username, 'testuser')

    def test_create_superuser(self):
        superuser = self.user_model.objects.create_superuser(username='admin', password='adminpass123')
        self.assertIsInstance(superuser, self.user_model)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_user_cpf_field(self):
        # Teste para verificar se o campo CPF está funcionando
        user = self.user_model.objects.create_user(username='cpfuser', password='testpass123', cpf='123.456.789-00')
        self.assertEqual(user.cpf, '123.456.789-00')

    def test_user_authentication(self):
        # Teste para verificar a autenticação do usuário
        user = self.user_model.objects.create_user(username='authuser', password='testpass123')
        self.assertTrue(self.client.login(username='authuser', password='testpass123'))

    def test_user_authentication_failure(self):
        # Teste para falha de autenticação
        self.assertFalse(self.client.login(username='wronguser', password='wrongpass'))

if __name__ == '__main__':
    import unittest
    unittest.main()