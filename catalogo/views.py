from datetime import date, timedelta

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from catalogo.models import Libro, Autor, InstanciaDeLibro, Genero, Lenguaje


def index(request):
    """View function para la pagina principal"""
    num_libros = Libro.objects.all().count()
    num_instancias = InstanciaDeLibro.objects.all().count()
    num_autores = Autor.objects.count() # 'all()' esta implicito

    num_instancias_disponibles = InstanciaDeLibro.objects.filter(estatus__exact='d').count()
    
    palabra = 'Harry' # input('Ingresa el título o una palabra del título para ser buscada:')
    num_libros_palabra = list(Libro.objects.filter(titulo__icontains=palabra).values_list('titulo'))

    contexto = {
        'num_libros': num_libros,
        'num_instancias': num_instancias,
        'num_autores': num_autores,
        'num_instancias_disponibles': num_instancias_disponibles,
        'num_libros_palabra': num_libros_palabra,
    }

    return render(request, 'index.html', context=contexto)


class VistaDeListaDeLibros(generic.ListView):
    """View function para todos los libros"""
    model = Libro
    context_object_name = 'lista_de_libros'
    template_name = 'libros/lista_de_libros.html'
    paginate_by = 10


class VistaDeDetallesDeLibros(generic.DetailView):
    """View function para los detalles de un libro"""
    model = Libro
    template_name = 'libros/detalle_del_libro.html'


class VistaDeListaDeAutores(generic.ListView):
    """View function para todos los autores"""
    model = Autor
    context_object_name = 'lista_de_autores'
    template_name = 'autores/lista_de_autores.html'
    paginate_by = 10


class VistaDeDetallesDeAutores(generic.DetailView):
    """View function para los detalles de un autor"""
    model = Autor
    template_name = 'autores/detalle_del_autor.html'


class VistaDeListaDeLibrosPrestados(LoginRequiredMixin, generic.ListView):
    """View function para mis prestamos"""
    model = InstanciaDeLibro
    context_object_name = 'instanciadelibro_lista'
    template_name = 'libros/instanciadelibro_lista_prestados_usuario.html'
    paginate_by = 10
    
    def get_queryset(self):
        return InstanciaDeLibro.objects.filter(prestatario=self.request.user).filter(estatus__exact='p').order_by('fecha_de_devolucion')


class VistaDePrestamosStaff(PermissionRequiredMixin, generic.ListView):
    """View function para todos los prestamos"""
    permission_required = 'catalogo.can_mark_returned'
    model = InstanciaDeLibro
    context_object_name = 'instanciadelibro_lista_staff'
    template_name = 'libros/instanciadelibro_lista_prestados_staff.html'
    paginate_by = 10
    
    def get_queryset(self):
        return InstanciaDeLibro.objects.filter(estatus__exact='p').order_by('fecha_de_devolucion')


class FormDevolverLibro(PermissionRequiredMixin, ModelForm):
    """Form function para devolver un prestamo a la libreria"""
    permission_required = 'catalogo.can_mark_returned'

    class Meta:
        model = InstanciaDeLibro
        fields = ['id']


def devolver_libro(request, pk):
    instancia_de_libro = get_object_or_404(InstanciaDeLibro, pk=pk)

    if request.method == 'POST':
        form = FormDevolverLibro(request.POST)

        instancia_de_libro.fecha_de_devolucion = date.today() + timedelta(weeks=2)
        instancia_de_libro.estatus = 'm'
        instancia_de_libro.prestatario = None
        instancia_de_libro.save()

        return HttpResponseRedirect(reverse('todoslosprestamos'))

    else:
        form = FormRenovarLibro()

        context = {
          'form': form,
          'instancia_de_libro': instancia_de_libro,
        }

        return render(request, 'libros/devolver_libro.html', context)


class FormRenovarLibro(PermissionRequiredMixin, ModelForm):
    """Form function para aplazar la fecha de devolucion un prestamo"""
    permission_required = 'catalogo.can_mark_returned'

    def clean_fecha_de_devolucion(self):
        data = self.cleaned_data['fecha_de_devolucion']

        if data < date.today() + timedelta(days=1):
            raise ValidationError('Fecha inválida - renovación en el pasado')

        if data > date.today() + timedelta(weeks=4):
            raise ValidationError('Fecha inválida - renovación con más de 4 semanas')

        return data

    class Meta:
        model = InstanciaDeLibro
        fields = ['fecha_de_devolucion']
        labels = {'fecha_de_devolucion': 'Fecha de renovacion'}
        help_texts = {'fecha_de_devolucion': 'Mínimo: mañana - Máximo: 4 semanas'} 


def renovar_libro(request, pk):
    instancia_de_libro = get_object_or_404(InstanciaDeLibro, pk=pk)
    fecha_de_renovacion_propuesta = date.today() + timedelta(weeks=3)
    form = FormRenovarLibro(initial={'fecha_de_devolucion': fecha_de_renovacion_propuesta})

    if request.method == 'POST':

        form = FormRenovarLibro(request.POST, initial={'fecha_de_devolucion': fecha_de_renovacion_propuesta})

        if form.is_valid():
            instancia_de_libro.fecha_de_devolucion = form.cleaned_data['fecha_de_devolucion']
            instancia_de_libro.save()

            return HttpResponseRedirect(reverse('todoslosprestamos'))

    context = {
      'form': form,
      'instancia_de_libro': instancia_de_libro,
    }

    return render(request, 'libros/renovar_libro.html', context)


class CrearLibro(PermissionRequiredMixin, CreateView):
    """View function para que staff pueda añadir un libro a la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Libro
    fields = '__all__'
    template_name = 'generic_form.html'


class ActualizarLibro(PermissionRequiredMixin, UpdateView):
    """View function para que staff pueda modificar un libro en la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Libro
    fields = '__all__'
    template_name = 'generic_form.html'


class EliminarLibro(PermissionRequiredMixin, DeleteView):
    """View function para que staff pueda eliminar un libro a la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Libro
    success_url = reverse_lazy('libros')
    template_name = 'libros/libro_confirm_delete.html'


class CrearAutor(PermissionRequiredMixin, CreateView):
    """View function para que staff pueda añadir un autor a la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Autor
    fields = '__all__'
    template_name = 'generic_form.html'


class ActualizarAutor(PermissionRequiredMixin, UpdateView):
    """View function para que staff pueda modificar un autor en la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Autor
    fields = '__all__'
    template_name = 'generic_form.html'


class EliminarAutor(PermissionRequiredMixin, DeleteView):
    """View function para que staff pueda eliminar un autor a la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = Autor
    success_url = reverse_lazy('autores')
    template_name = 'autores/autor_confirm_delete.html'


class CrearPrestamo(PermissionRequiredMixin, CreateView):
    """View function para que staff pueda añadir una instancia de libro a la base de datos"""
    permission_required = 'catalogo.can_mark_returned'
    model = InstanciaDeLibro
    fields = '__all__'
    template_name = 'generic_form.html'
