from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.VistaDeListaDeLibros.as_view(), name='libros'),
    path('libros/crear/', views.CrearLibro.as_view(), name='libro_crear'),
    path('libros/<int:pk>', views.VistaDeDetallesDeLibros.as_view(), name='detalle_del_libro'),
    path('libros/<int:pk>/actualizar/', views.ActualizarLibro.as_view(), name='libro_actualizar'),
    path('libros/<int:pk>/eliminar/', views.EliminarLibro.as_view(), name='libro_eliminar'),
    path('libros/<uuid:pk>/devolver/', views.devolver_libro, name='devolver_libro'),
    path('libros/<uuid:pk>/renovar/', views.renovar_libro, name='renovar_libro'),
    path('autores/', views.VistaDeListaDeAutores.as_view(), name='autores'),
    path('autores/crear/', views.CrearAutor.as_view(), name='autor_crear'),
    path('autores/<int:pk>', views.VistaDeDetallesDeAutores.as_view(), name='detalle_del_autor'),
    path('autores/<int:pk>/actualizar/', views.ActualizarAutor.as_view(), name='autor_actualizar'),
    path('autores/<int:pk>/eliminar/', views.EliminarAutor.as_view(), name='autor_eliminar'),
    path('mislibros/', views.VistaDeListaDeLibrosPrestados.as_view(), name='misprestamos'),
    path('prestamos/', views.VistaDePrestamosStaff.as_view(), name='todoslosprestamos'),
    path('prestamos/crear/', views.CrearPrestamo.as_view(), name='prestamo_crear'),
]
