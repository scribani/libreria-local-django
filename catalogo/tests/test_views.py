from datetime import date, timedelta
import uuid

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from catalogo.models import Libro, Autor, InstanciaDeLibro, Genero, Lenguaje


def create_book(*args):
    test_autor = Autor.objects.create(nombre=f'Carlos {args[0]}', apellido=f'Perez {args[0]}')
    test_lenguaje = Lenguaje.objects.create(nombre='Español')
    test_genero = Genero.objects.create(nombre='Ficción')
    test_libro = Libro.objects.create(
      titulo=f'Mi libro de pruebas {args[0]}',
      resumen='Resumen de mi libro',
      isbn=9781234567890,
      autor=test_autor,
      lenguaje=test_lenguaje,
    )

    genero_para_libros = Genero.objects.all()
    test_libro.genero.set(genero_para_libros) # Asignacion del genero como paso extra porque es de tipo many-to-many
    test_libro.save()

    return test_libro    


def log_in_assertion(
  obj,
  username,
  password,
  path_name,
  **kwargs,
):
    if not kwargs:
        login = obj.client.login(username=username, password=password)
        response = obj.client.get(reverse(path_name))

        obj.assertEqual(str(response.context['user']), username)
        obj.assertEqual(response.status_code, 200)
    
    else:
        login = obj.client.login(username=username, password=password)
        response = obj.client.get(reverse(path_name, kwargs={'pk': kwargs['pk']}))

    return response


def exists_at_location(
  obj,
  path,
  logged_in_necessary=False,
  **kwargs,
):
    if logged_in_necessary:
        log_in_assertion(
          obj,
          kwargs['username'],
          kwargs['password'],
          kwargs['path_name']
        )

    response = obj.client.get(path)
    obj.assertEqual(response.status_code, 200)


def accessible_by_name(
  obj,
  logged_in_necessary=False,
  **kwargs,
  ):
    if not logged_in_necessary:
        response = obj.client.get(reverse(kwargs['path_name']))
        obj.assertEqual(response.status_code, 200)

    else:
        log_in_assertion(
          obj,
          kwargs['username'],
          kwargs['password'],
          kwargs['path_name']
        )


def uses_correct_template(
  obj,
  template,
  logged_in_necessary=False,
  **kwargs,
):
    if not logged_in_necessary:
      response = obj.client.get(reverse(kwargs['path_name']))
      obj.assertEqual(response.status_code, 200)

    else:
        response = log_in_assertion(
          obj,
          kwargs['username'],
          kwargs['password'],
          kwargs['path_name'],
        )

    obj.assertTemplateUsed(response, template)


def pagination_is_ten(
  obj,
  context_object_name,
  logged_in_necessary=False,
  **kwargs,
):
    if not logged_in_necessary:
        response = obj.client.get(reverse(kwargs['path_name']))
        obj.assertEqual(response.status_code, 200)

    else:
        response = log_in_assertion(
          obj,
          kwargs['username'],
          kwargs['password'],
          kwargs['path_name']
        )

    obj.assertTrue('is_paginated' in response.context)
    obj.assertTrue(response.context['is_paginated'] == True)
    obj.assertEqual(len(response.context[context_object_name]), 10)


def redirect_if_not_logged_in(
  obj,
  path,
  path_name,
  **kwargs,
):
    if not kwargs:
      response = obj.client.get(reverse(path_name))
      obj.assertRedirects(response, f'/accounts/login/?next=/catalogo/{path}')

    else:
      response = obj.client.get(reverse(path_name, kwargs={'pk': kwargs['pk']}))
      obj.assertEqual(response.status_code, 302)
      obj.assertTrue(response.url.startswith('/accounts/login/'))


class ListaDeLibrosViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        numero_de_libros = 15
        
        for libro_id in range(numero_de_libros):
            create_book(libro_id)

    def test_exists_at_location(self):
        exists_at_location(self, '/catalogo/libros/')

    def test_accessible_by_name(self):
        accessible_by_name(self, path_name='libros')

    def test_uses_correct_template(self):
        uses_correct_template(self, 'libros/lista_de_libros.html', path_name='libros')

    def test_pagination_is_ten(self):
        pagination_is_ten(self, 'lista_de_libros', path_name='libros')


class ListaDeAutoresViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        numero_de_autores = 15
        
        for autor_id in range(numero_de_autores):
            Autor.objects.create(nombre=f'Carlos {autor_id}', apellido=f'Perez {autor_id}',)

    def test_exists_at_location(self):
        exists_at_location(self, '/catalogo/autores/')

    def test_accessible_by_name(self):
        accessible_by_name(self, path_name='autores')

    def test_uses_correct_template(self):
        uses_correct_template(self, 'autores/lista_de_autores.html', path_name='autores')

    def test_pagination_is_ten(self):
        pagination_is_ten(self, 'lista_de_autores', path_name='autores')


class ListaDeLibrosPrestadosViewTest(TestCase):
    def setUp(self):
        test_user_1 = User.objects.create_user(username='testuser1', password='XmCDhM7Z!k4d')
        test_user_1.save()

        test_user_2 = User.objects.create_user(username='testuser2', password='u4JdcmLXC3^r')
        test_user_2.save()

        test_libro = create_book(1)
        numero_de_libros = 30

        for copia in range(numero_de_libros):
            fecha_de_devolucion = date.today() + timedelta(days=copia%5)
            prestatario = [test_user_1, test_user_2][copia % 2 == 0]
            InstanciaDeLibro.objects.create(
              libro=test_libro,
              fecha_de_devolucion=fecha_de_devolucion,
              prestatario=prestatario,
              estatus='p',
            )

    def test_exists_at_location(self):
        exists_at_location(
          self,
          '/catalogo/mislibros/',
          logged_in_necessary=True,
          username='testuser1',
          password='XmCDhM7Z!k4d',
          path_name='misprestamos',
        )

    def test_accessible_by_name(self):
        accessible_by_name(
          self,
          logged_in_necessary=True,
          username='testuser1',
          password='XmCDhM7Z!k4d',
          path_name='misprestamos',
        )

    def test_uses_correct_template(self):
        uses_correct_template(
          self,
          'libros/instanciadelibro_lista_prestados_usuario.html',
          logged_in_necessary=True,
          username='testuser1',
          password='XmCDhM7Z!k4d',
          path_name='misprestamos',
        )

    def test_pagination_is_ten(self):
        pagination_is_ten(
          self,
          'instanciadelibro_lista',
          logged_in_necessary=True,
          username='testuser1',
          password='XmCDhM7Z!k4d',
          path_name='misprestamos',
        )

    def test_redirect_if_not_logged_in(self):
        redirect_if_not_logged_in(self, 'mislibros/', 'misprestamos')

    def test_only_mislibros_in_list(self):
        response = log_in_assertion(self, 'testuser1', 'XmCDhM7Z!k4d', 'misprestamos')

        self.assertTrue('instanciadelibro_lista' in response.context)

        for copia in response.context['instanciadelibro_lista']:
            self.assertEqual(response.context['user'], copia.prestatario)
            self.assertEqual('p', copia.estatus)
    
    def test_ordered_by_fecha_de_devolucion(self):
        response = log_in_assertion(
          self,
          'testuser1',
          'XmCDhM7Z!k4d',
          'misprestamos',
        )

        ultima_fecha = 0
        for copia in response.context['instanciadelibro_lista']:
            if ultima_fecha == 0:
                ultima_fecha = copia.fecha_de_devolucion
            else:
                self.assertTrue(ultima_fecha <= copia.fecha_de_devolucion)
                ultima_fecha = copia.fecha_de_devolucion


class PrestamosStaffViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='$KN9vq4PlrXM')
        test_user.save()

        test_staff = User.objects.create_user(username='teststaff', password='9@nG5!kcffe$')
        test_staff.save()

        test_permission = Permission.objects.get(name='Can set book as returned')
        test_staff.user_permissions.add(test_permission)
        test_staff.save()

        test_libro = create_book(1)
        numero_de_libros = 30

        for copia in range(numero_de_libros):
            fecha_de_devolucion = date.today() + timedelta(weeks=3)
            InstanciaDeLibro.objects.create(
              libro=test_libro,
              fecha_de_devolucion=fecha_de_devolucion,
              prestatario=test_user,
              estatus=['p', 'm'][copia % 2 == 0]
            )

    def test_exists_at_location(self):
        exists_at_location(
          self,
          '/catalogo/prestamos/',
          logged_in_necessary=True,
          username='teststaff',
          password='9@nG5!kcffe$',
          path_name='todoslosprestamos',
        )

    def test_accessible_by_name(self):
        accessible_by_name(
          self,
          logged_in_necessary=True,
          username='teststaff',
          password='9@nG5!kcffe$',
          path_name='todoslosprestamos',
        )

    def test_uses_correct_template(self):
        uses_correct_template(
          self,
          'libros/instanciadelibro_lista_prestados_staff.html',
          logged_in_necessary=True,
          username='teststaff',
          password='9@nG5!kcffe$',
          path_name='todoslosprestamos',
        )

    def test_pagination_is_ten(self):
        pagination_is_ten(
          self,
          'instanciadelibro_lista_staff',
          logged_in_necessary=True,
          username='teststaff',
          password='9@nG5!kcffe$',
          path_name='todoslosprestamos',
        )

    def test_redirect_if_not_logged_in(self):
        redirect_if_not_logged_in(self, 'prestamos/', 'todoslosprestamos')

    def test_only_prestados_in_list(self):
        response = log_in_assertion(
          self,
          'teststaff',
          '9@nG5!kcffe$',
          'todoslosprestamos'
        )

        self.assertTrue('instanciadelibro_lista_staff' in response.context)

        for copia in response.context['instanciadelibro_lista_staff']:
            self.assertEqual('p', copia.estatus)
    
    def test_ordered_by_fecha_de_devolucion(self):
        response = log_in_assertion(
          self,
          'teststaff',
          '9@nG5!kcffe$',
          'todoslosprestamos'
        )

        ultima_fecha = 0
        for copia in response.context['instanciadelibro_lista_staff']:
            if ultima_fecha == 0:
                ultima_fecha = copia.fecha_de_devolucion
            else:
                self.assertTrue(ultima_fecha <= copia.fecha_de_devolucion)
                ultima_fecha = copia.fecha_de_devolucion


class RenovarLibroViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='Irdw8@1F5Il^')
        test_user.save()

        test_staff = User.objects.create_user(username='teststaff', password='R*Cr44061FP0')
        test_staff.save()

        test_permission = Permission.objects.get(name='Can set book as returned')
        test_staff.user_permissions.add(test_permission)
        test_staff.save()

        test_libro = create_book(1)

        fecha_de_devolucion = date.today() + timedelta(days=5)
        self.test_instancia1 = InstanciaDeLibro.objects.create(
          libro=test_libro,
          fecha_de_devolucion=fecha_de_devolucion,
          prestatario=test_user,
          estatus='p',
        )

        fecha_de_devolucion = date.today() + timedelta(days=5)
        self.test_instancia2 = InstanciaDeLibro.objects.create(
          libro=test_libro,
          fecha_de_devolucion=fecha_de_devolucion,
          prestatario=test_staff,
          estatus='p',
        )

    def test_uses_correct_template(self):
        response = log_in_assertion(
          self,
          'teststaff',
          'R*Cr44061FP0',
          'renovar_libro',
          pk=self.test_instancia2.id,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/renovar_libro.html')

    def test_redirect_if_not_logged_in(self):
        redirect_if_not_logged_in(
          self,
          None,
          'renovar_libro',
          pk=self.test_instancia1.id,
        )

    def test_redirect_if_logged_in_but_forbidden_user(self):
        response = log_in_assertion(
          self,
          'testuser',
          'Irdw8@1F5Il^',
          'renovar_libro',
          pk=self.test_instancia1.id,
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permissions(self):
        response_miprestamo = log_in_assertion(
          self,
          'teststaff',
          'R*Cr44061FP0',
          'renovar_libro',
          pk=self.test_instancia2.id,
        )

        response_otroprestamo = log_in_assertion(
          self,
          'teststaff',
          'R*Cr44061FP0',
          'renovar_libro',
          pk=self.test_instancia1.id,
        )
        
        self.assertEqual(response_miprestamo.status_code, 200)
        self.assertEqual(response_otroprestamo.status_code, 200)

    def test_404_for_invalid_book_if_logged_in(self):
        test_uuid = uuid.uuid4()
        response = log_in_assertion(
          self,
          'teststaff',
          'R*Cr44061FP0',
          'renovar_libro',
          pk=test_uuid,
        )

        self.assertEqual(response.status_code, 404)

    def test_fecha_de_renovacion_initial(self):
        response = log_in_assertion(
          self,
          'teststaff',
          'R*Cr44061FP0',
          'renovar_libro',
          pk=self.test_instancia2.id,
        )
        fecha_de_renovacion = date.today() + timedelta(weeks=3)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['fecha_de_devolucion'], fecha_de_renovacion)

    def test_invalid_fecha_de_renovacion(self):
        login = self.client.login(username='teststaff', password='R*Cr44061FP0')
        fecha_de_renovacion_pasada = date.today() - timedelta(weeks=2)
        fecha_de_renovacion_lejana = date.today() + timedelta(weeks=9)
        response_pasada = self.client.post(reverse('renovar_libro', kwargs={'pk': self.test_instancia2.id}), {'fecha_de_devolucion': fecha_de_renovacion_pasada})
        response_lejana = self.client.post(reverse('renovar_libro', kwargs={'pk': self.test_instancia2.id}), {'fecha_de_devolucion': fecha_de_renovacion_lejana})

        self.assertEqual(response_pasada.status_code, 200)
        self.assertFormError(
          response_pasada,
          'form',
          'fecha_de_devolucion',
          'Fecha inválida - renovación en el pasado'
        )
        self.assertEqual(response_lejana.status_code, 200)
        self.assertFormError(
          response_lejana,
          'form',
          'fecha_de_devolucion',
          'Fecha inválida - renovación con más de 4 semanas'
        )

    def test_redirect_correctly_on_success(self):
        login = self.client.login(username='teststaff', password='R*Cr44061FP0')
        fecha_de_renovacion_valida = date.today() + timedelta(weeks=2)
        response = self.client.post(reverse('renovar_libro', kwargs={'pk': self.test_instancia2.id}), {'fecha_de_devolucion': fecha_de_renovacion_valida})

        self.assertRedirects(response, reverse('todoslosprestamos'))


class DevolverLibroViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='AK6g4#m$&08r')
        test_user.save()

        test_staff = User.objects.create_user(username='teststaff', password='QZ7v1%lv3Wpc')
        test_staff.save()

        test_permission = Permission.objects.get(name='Can set book as returned')
        test_staff.user_permissions.add(test_permission)
        test_staff.save()

        test_libro = create_book(1)

        fecha_de_devolucion = date.today() + timedelta(days=5)
        self.test_instancia = InstanciaDeLibro.objects.create(
          libro=test_libro,
          fecha_de_devolucion=fecha_de_devolucion,
          prestatario=test_user,
          estatus='p',
        )

    def test_uses_correct_template(self):
        response = log_in_assertion(
          self,
          'teststaff',
          'QZ7v1%lv3Wpc',
          'devolver_libro',
          pk=self.test_instancia.id,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/devolver_libro.html')

    def test_redirect_if_not_logged_in(self):
        redirect_if_not_logged_in(
          self,
          None,
          'devolver_libro',
          pk=self.test_instancia.id,
        )

    def test_redirect_if_logged_in_but_forbidden_user(self):
        response = log_in_assertion(
          self,
          'testuser',
          'AK6g4#m$&08r',
          'devolver_libro',
          pk=self.test_instancia.id,
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permissions(self):
        response = log_in_assertion(
          self,
          'teststaff',
          'QZ7v1%lv3Wpc',
          'devolver_libro',
          pk=self.test_instancia.id,
        )
        
        self.assertEqual(response.status_code, 200)

    def test_404_for_invalid_book_if_logged_in(self):
        test_uuid = uuid.uuid4()
        response = log_in_assertion(
          self,
          'teststaff',
          'QZ7v1%lv3Wpc',
          'devolver_libro',
          pk=test_uuid,
        )

        self.assertEqual(response.status_code, 404)

    def test_redirect_correctly_on_success(self):
        login = self.client.login(username='teststaff', password='QZ7v1%lv3Wpc')
        response = self.client.post(reverse('devolver_libro', kwargs={'pk': self.test_instancia.id}))

        self.assertRedirects(response, reverse('todoslosprestamos'))
