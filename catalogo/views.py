from django.shortcuts import render
from catalogo.models import Libro, Autor, InstanciaDeLibro, Genero, Lenguaje
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def index(request):
    """View function para la pagina principal"""
    num_libros = Libro.objects.all().count()
    num_instancias = InstanciaDeLibro.objects.all().count()
    num_autores = Autor.objects.count() # 'all()' esta implicito

    num_instancias_disponibles = InstanciaDeLibro.objects.filter(estatus__exact='d').count()
    
    palabra = 'era' # input('Ingresa el título o una palabra del título para ser buscada:')
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
    model = Libro
    context_object_name = 'lista_de_libros'
    template_name = 'libros/lista_de_libros.html'
    paginate_by = 2


class VistaDeDetallesDeLibros(generic.DetailView):
    model = Libro
    template_name = 'libros/detalle_del_libro.html'


class VistaDeListaDeAutores(generic.ListView):
    model = Autor
    context_object_name = 'lista_de_autores'
    template_name = 'autores/lista_de_autores.html'
    paginate_by = 2


class VistaDeDetallesDeAutores(generic.DetailView):
    model = Autor
    template_name = 'autores/detalle_del_autor.html'


class VistaDeListaDeLibrosPrestados(LoginRequiredMixin, generic.ListView):
    model = InstanciaDeLibro
    context_object_name = 'instanciadelibro_lista'
    template_name = 'libros/instanciadelibro_lista_prestados_usuario.html'
    paginate_by = 10
    
    def get_queryset(self):
        return InstanciaDeLibro.objects.filter(prestatario=self.request.user).filter(estatus__exact='p').order_by('fecha_de_devolucion')


class VistaDePrestamosStaff(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalogo.can_mark_returned'
    model = InstanciaDeLibro
    context_object_name = 'instanciadelibro_lista_staff'
    template_name = 'libros/instanciadelibro_lista_prestados_staff.html'
    paginate_by = 10
    
    def get_queryset(self):
        return InstanciaDeLibro.objects.filter(estatus__exact='p').order_by('fecha_de_devolucion')

