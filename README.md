# Librería Local

[![made-with-django](https://img.shields.io/badge/Django-2.2-blue)](https://http://www.djangoproject.com/) [![made-with-python](https://img.shields.io/badge/Python-3.8-blue)](https://www.python.org/) [![coverage](https://img.shields.io/badge/coverage-98%25-green)](https://i.imgur.com/JpooKE2.png)
-

Página web de una librería ficticia para gestionar los préstamos y los libros de dicho establecimiento.

Permite que los bibliotecarios puedan realizar todas las acciones necesarias para controlar la distribución de las copias de los libros (introducir nuevos titulos a la base de datos, indicar el numero de copias para cada titulo, realizar prestamos y recibir devoluciones, etc).

Del modo similar, permite que los usuarios puedan ver los libros, autores, idiomas y generos disponibles en la libreria, asi como visualizar los prestamos a su nombre y su respectiva fecha de devolucion.

## Uso

### Si desea utilizar la base datos proporcionada:

1. Ejecute los siguientes comandos en el directorio del proyecto (si usted usa Windows intente reemplazar ```python``` por ```py``` o ```py -3```)

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
python manage.py runserver
```

2. Abra una ventana en su navegador con http://127.0.0.1:8000/ para visualizar la pagina principal.

3. Para iniciar sesion como **bibliotecario**, haga click sobre ***Iniciar sesion*** e ingrese los siguientes datos:

        Nombre de usuario: fernanda
        Contraseña: usertest


        # Para iniciar sesion como usuario:
        Nombre de usuario: manuel
        Contraseña: usertest

    **Para acceder a la pagina administrativa del sitio ingrese a http://127.0.0.1:8000/admin/ con la siguiente informacion:**

        Nombre de usuario: admin
        Contraseña: test
---
### Si desea crear su propia base de datos:

1. Ejecute los siguientes comandos en el directorio del proyecto (si usted usa Windows intente reemplazar ```python``` por ```py``` o ```py -3```)

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

2. Abra en su navegador http://127.0.0.1:8000/admin/

3. Cree algunos objetos para cada tipo

4. Vaya al sitio principal (http://127.0.0.1:8000/) para interactuar con sus nuevos objetos

