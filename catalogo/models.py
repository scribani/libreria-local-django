from django.db import models
from django.urls import reverse
import uuid # Requerido para definir instancias unicas por libro


class Genero(models.Model):
    """Modelo que representa un genero de libro"""
    nombre = models.CharField(max_length=200, help_text='Ingresa un género de libro (ejemplo: Ciencia Ficción)')

    def __str__(self):
        return self.nombre


class Lenguaje(models.Model):
    """Modelo que representa un lenguaje"""
    nombre = models.CharField(max_length=200, help_text='Ingresa el Lenguaje natural de un libro (ejemplo: Español)')

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    """Modelo que representa un libro (pero no una copia especifica del libro)"""
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    resumen = models.TextField(max_length=1000, help_text='Ingresa una breve descripción del libro')
    isbn = models.CharField('ISBN', max_length=13, help_text='Ingresa el <a href="https://www.isbn-international.org/es/content/¿que-es-un-isbn">número ISBN</a> de 13 carácteres')
    lenguaje = models.ForeignKey('Lenguaje', on_delete=models.SET_NULL, null=True)
    genero = models.ManyToManyField(Genero, help_text='Selecciona un género para este libro')

    
    def desplegar_genero(self):
        """Crea un string para el Genero. Se requiere para desplegar genero en Admin"""
        return ', '.join(genero.nombre for genero in self.genero.all()[:3])
    
    desplegar_genero.short_description = 'Genero'
    
    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('detalle_del_libro', args=[str(self.id)])


class InstanciaDeLibro(models.Model):
    """Modelo que representa una copia especifica de un libro (ejemplo: un libro prestado por la libreria)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID único para este libro en particular en toda la librería')
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True) 
    fecha_de_devolucion = models.DateField(null=True, blank=True)

    ESTADO_DEL_PRESTAMO = (
        ('m', 'Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estatus = models.CharField(
        max_length=1,
        choices=ESTADO_DEL_PRESTAMO,
        blank=True,
        default=' ',
        help_text='Disponibilidad del libro',
    )

    class Meta:
        ordering = ['fecha_de_devolucion']

    def __str__(self):
        return f'{self.libro.titulo} ({self.id})'


class Autor(models.Model):
    """Modelo que representa un autor"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    fecha_de_deceso = models.DateField('Fallecimiento', null=True, blank=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def get_absolute_url(self):
        return reverse('detalle_del_autor', args=[str(self.id)])

    def __str__(self):
        return f'{self.apellido}, {self.nombre}'

