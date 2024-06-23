from django.test import TestCase
from django.utils import timezone
from .models import Cursos, Aulas, Comentarios, NotasAulas, ProgressoAula
from usuarios.models import USUARIO

class CursosModelTest(TestCase):

    def setUp(self):
        self.curso = Cursos.objects.create(
            nome="Curso de Django",
            descricao="Curso avançado de Django",
            thumb="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            ativo=True
        )

    def test_create_curso(self):
        self.assertEqual(self.curso.nome, "Curso de Django")
        self.assertTrue(self.curso.ativo)
        self.assertEqual(str(self.curso), self.curso.nome)

class AulasModelTest(TestCase):

    def setUp(self):
        self.curso = Cursos.objects.create(
            nome="Curso de Django",
            descricao="Curso avançado de Django",
            thumb="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            ativo=True
        )
        self.aula = Aulas.objects.create(
            nome="Aula 1",
            descricao="Introdução ao Django",
            aula="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            curso=self.curso,
            data_upload=timezone.now(),
            ativo=True
        )

    def test_create_aula(self):
        self.assertEqual(self.aula.nome, "Aula 1")
        self.assertTrue(self.aula.ativo)
        self.assertEqual(str(self.aula), self.aula.nome)

class ComentariosModelTest(TestCase):

    def setUp(self):
        self.usuario = USUARIO.objects.create_user(username='testuser', password='12345')
        self.curso = Cursos.objects.create(
            nome="Curso de Django",
            descricao="Curso avançado de Django",
            thumb="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            ativo=True
        )
        self.aula = Aulas.objects.create(
            nome="Aula 1",
            descricao="Introdução ao Django",
            aula="path/to/aula.mp4",
            curso=self.curso,
            data_upload=timezone.now(),
            ativo=True
        )
        self.comentario = Comentarios.objects.create(
            usuario=self.usuario,
            comentario="Excelente aula!",
            data=timezone.now(),
            aula=self.aula
        )

    def test_create_comentario(self):
        self.assertEqual(self.comentario.comentario, "Excelente aula!")
        self.assertEqual(str(self.comentario), str(self.usuario))

class NotasAulasModelTest(TestCase):

    def setUp(self):
        self.usuario = USUARIO.objects.create_user(username='testuser', password='12345')
        self.curso = Cursos.objects.create(
            nome="Curso de Django",
            descricao="Curso avançado de Django",
            thumb="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            ativo=True
        )
        self.aula = Aulas.objects.create(
            nome="Aula 1",
            descricao="Introdução ao Django",
            aula="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            curso=self.curso,
            data_upload=timezone.now(),
            ativo=True
        )
        self.nota = NotasAulas.objects.create(
            aula=self.aula,
            nota='b',
            usuario=self.usuario
        )

    def test_create_nota(self):
        self.assertEqual(self.nota.nota, 'b')
        self.assertEqual(str(self.nota), str(self.usuario))

class ProgressoAulaModelTest(TestCase):

    def setUp(self):
        self.usuario = USUARIO.objects.create_user(username='testuser', password='12345')
        self.curso = Cursos.objects.create(
            nome="Curso de Django",
            descricao="Curso avançado de Django",
            thumb="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            ativo=True
        )
        self.aula = Aulas.objects.create(
            nome="Aula 1",
            descricao="Introdução ao Django",
            aula="/media/aulas/Screenshot_from_2024-06-14_10-46-04.png",
            curso=self.curso,
            data_upload=timezone.now(),
            ativo=True
        )
        self.progresso = ProgressoAula.objects.create(
            usuario=self.usuario,
            aula=self.aula,
            concluida=True,
            baixou_certificado=False
        )

    def test_create_progresso(self):
        self.assertTrue(self.progresso.concluida)
        self.assertFalse(self.progresso.baixou_certificado)
        self.assertEqual(str(self.progresso), f"{self.usuario.username} - {self.aula.nome}")


from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Cursos, Aulas, ProgressoAula


class BaixarCertificadoViewTest(TestCase):

    def setUp(self):
        # Criar um usuário e fazer login
        self.user = get_user_model().objects.create_user(username='testuser', password='12345', first_name='Test')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        
        # Criar um curso e uma aula
        self.curso = Cursos.objects.create(
            nome="Curso de Teste",
            descricao="Descrição do Curso de Teste",
            thumb="path/to/image.jpg",
            ativo=True
        )
        self.aula = Aulas.objects.create(
            nome="Aula de Teste",
            descricao="Descrição da Aula de Teste",
            aula="path/to/aula.mp4",
            curso=self.curso,
            ativo=True
        )
        
        # Criar um progresso de aula
        self.progresso = ProgressoAula.objects.create(
            usuario=self.user,
            aula=self.aula,
            concluida=True,
            baixou_certificado=False
        )

    def test_baixar_certificado(self):
        # Fazer uma solicitação para a view baixar_certificado
        self.progresso.baixou_certificado=True

        response = self.client.get('baixar_certificado/', args=[self.curso.id])

        # Verificar se o progresso foi atualizado corretamente
        self.progresso.refresh_from_db()
        self.assertTrue(self.progresso.baixou_certificado)

        # Verificar se a resposta é um arquivo PDF
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn(f'attachment; filename="Certificado({self.user}).pdf"', response['Content-Disposition'])