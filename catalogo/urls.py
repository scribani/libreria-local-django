from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.VistaDeListaDeLibros.as_view(), name='libros'),
    path('libros/<int:pk>', views.VistaDeDetallesDeLibros.as_view(), name='detalle_del_libro'),
    path('autores/', views.VistaDeListaDeAutores.as_view(), name='autores'),
    path('autores/<int:pk>', views.VistaDeDetallesDeAutores.as_view(), name='detalle_del_autor'),
    path('mislibros/', views.VistaDeListaDeLibrosPrestados.as_view(), name='misprestamos'),
    path('prestamos/', views.VistaDePrestamosStaff.as_view(), name='todoslosprestamos'),
]

