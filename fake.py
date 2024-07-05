
def main():
    fake = Faker()
 ##  for _ in range(10):
  #     cursos = Cursos.objects.create(
  #     nome=fake.name(),
  #     descricao=fake.text(),
  #     thumb = 'media/thumb_cursos/Cursos-NR-35-Trabalho-em-Altura_7JH4rc4.jpg',
  #     cargoraria = 2,
  #     validade = 5,
  #     ativo= True
  #     )
  #     print(f'curso criado {cursos}')

  #  todos_cursos = Cursos.objects.all()

  # for _ in range(150):
  #     aulas = Aulas.objects.create(
  #     nome = fake.name(),
  #     descricao = fake.name(),
  #     aula = 'media/aulas/2024-07-01_11-06-35.mp4',
  #     curso = random.choice(todos_cursos)
  #     )
  #     print(f'aula criada{aulas}')

    for _ in range(50):
        usuarios = USUARIO.objects.create(
        username=fake.name(),
        first_name=fake.name(),
        email=fake.email(),
        cpf=fake.numerify(text='###########'),
        password='Senha123@',
    )
        print(f'usuario{usuarios}')


if __name__ == '__main__':
    import os
    import random
    from django.core.wsgi import get_wsgi_application
 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_cursos.settings')
    application = get_wsgi_application()
    from cursos.models import Cursos,Aulas
    from usuarios.models import USUARIO
    from faker import Faker
    from datetime import date ,timedelta

    main()