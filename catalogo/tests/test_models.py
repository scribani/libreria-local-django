import uuid

from django.test import TestCase

from catalogo.models import Libro, Autor, InstanciaDeLibro, Genero, Lenguaje


def list_assertion(obj, fields, names):
    for idx, field in enumerate(fields):
        obj.assertEqual(field, names[idx])


class GeneroModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genero.objects.create(nombre='Ciencia Ficción')

    def test_str_representation(self):
        genero = Genero.objects.get(id=1)
        expected_object_name = f'{genero.nombre}'

        self.assertEqual(expected_object_name, str(genero))


class LenguajeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Lenguaje.objects.create(nombre='Italiano')

    def test_str_representation(self):
        lenguaje = Lenguaje.objects.get(id=1)
        expected_object_name = f'{lenguaje.nombre}'

        self.assertEqual(expected_object_name, str(lenguaje))


class LibroModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Libro.objects.create(titulo='Mi libro de prueba')

    def test_labels(self):
        libro = Libro.objects.get(id=1)
        field_label_titulo = libro._meta.get_field('titulo').verbose_name
        field_label_autor = libro._meta.get_field('autor').verbose_name
        field_label_lenguaje = libro._meta.get_field('lenguaje').verbose_name
        field_label_genero = libro._meta.get_field('genero').verbose_name

        fields = [
          field_label_titulo,
          field_label_autor,
          field_label_lenguaje,
          field_label_genero,
        ]
        names = [
          'titulo',
          'autor',
          'lenguaje',
          'genero',
        ]

        list_assertion(self, fields, names)

    def test_resumen_and_isbn_max_length(self):
        libro = Libro.objects.get(id=1)
        field_label_resumen = libro._meta.get_field('resumen').max_length
        field_label_isbn = libro._meta.get_field('isbn').max_length

        self.assertEqual(field_label_resumen, 1000)
        self.assertEqual(field_label_isbn, 13)

    def test_str_representation(self):
        libro = Libro.objects.get(id=1)
        expected_object_name = f'{libro.titulo}'

        self.assertEqual(expected_object_name, str(libro))

    def test_get_absolute_url(self):
        libro = Libro.objects.get(id=1)

        self.assertEqual(libro.get_absolute_url(), '/catalogo/libros/1')


class InstanciaDeLibroModelTest(TestCase):
    test_id = uuid.uuid4()

    @classmethod
    def setUpTestData(cls, test_id=test_id):
        libro = Libro.objects.create(titulo='Mi libro de prueba')
        InstanciaDeLibro.objects.create(id=test_id, libro=libro)

    def test_labels(self, test_id=test_id):
        instancia_de_libro = InstanciaDeLibro.objects.get(id=test_id)
        field_label_id = instancia_de_libro._meta.get_field('id').verbose_name
        field_label_libro = instancia_de_libro._meta.get_field('libro').verbose_name
        field_label_fecha_de_devolucion = instancia_de_libro._meta.get_field('fecha_de_devolucion').verbose_name
        field_label_prestatario = instancia_de_libro._meta.get_field('prestatario').verbose_name
        field_label_estatus = instancia_de_libro._meta.get_field('estatus').verbose_name

        fields = [
          field_label_id,
          field_label_libro,
          field_label_fecha_de_devolucion,
          field_label_prestatario,
          field_label_estatus,
        ]
        names = [
          'id',
          'libro',
          'fecha de devolucion',
          'prestatario',
          'estatus',
        ]

        list_assertion(self, fields, names)
        
    def test_str_representation(self, test_id=test_id):
        instancia_de_libro = InstanciaDeLibro.objects.get(id=test_id)
        expected_object_name = f'{instancia_de_libro.libro.titulo} ({instancia_de_libro.id})'
        
        self.assertEqual(expected_object_name, str(instancia_de_libro))


class AutorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Autor.objects.create(nombre='Jose', apellido='Perez')

    def test_labels(self):
        autor = Autor.objects.get(id=1)
        field_label_nombre = autor._meta.get_field('nombre').verbose_name
        field_label_apellido = autor._meta.get_field('apellido').verbose_name
        field_label_fecha_de_nacimiento = autor._meta.get_field('fecha_de_nacimiento').verbose_name
        field_label_fecha_de_deceso = autor._meta.get_field('fecha_de_deceso').verbose_name

        fields = [
          field_label_nombre,
          field_label_apellido,
          field_label_fecha_de_nacimiento,
          field_label_fecha_de_deceso,
        ]
        names = [
          'nombre',
          'apellido',
          'fecha de nacimiento',
          'Fallecimiento',
        ]

        list_assertion(self, fields, names)

    def test_full_name_max_length(self):
        autor = Autor.objects.get(id=1)
        field_label_nombre = autor._meta.get_field('nombre').max_length
        field_label_apellido = autor._meta.get_field('apellido').max_length

        self.assertEqual(field_label_nombre, 100)
        self.assertEqual(field_label_apellido, 100)

    def test_str_representation(self):
        autor = Autor.objects.get(id=1)
        expected_object_name = f'{autor.apellido}, {autor.nombre}'

        self.assertEqual(expected_object_name, str(autor))

    def test_get_absolute_url(self):
        autor = Autor.objects.get(id=1)

        self.assertEqual(autor.get_absolute_url(), '/catalogo/autores/1')
