# Librería Local

Página web de una librería ficticia para gestionar los préstamos y los libros de dicho establecimiento.

Permite que los bibliotecarios puedan realizar todas las acciones necesarias para controlar la distribución de las copias de los libros (introducir nuevos títulos a la base de datos, indicar el número de copias para cada titulo, realizar préstamos y recibir devoluciones, etc).

De modo similar, permite que los usuarios puedan ver los libros y autores disponibles en la librería, asi como visualizar los préstamos a su nombre y su respectiva fecha de devolución.

## Uso

### Si desea utilizar la base datos proporcionada:

1. Ejecute los siguientes comandos en el directorio del proyecto (si usted usa Windows intente reemplazar `python` por `py` o `py -3`)

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
python manage.py runserver
```

2. Abra una ventana en su navegador con http://127.0.0.1:8000/ para visualizar la página principal.

3. Para iniciar sesión como **bibliotecario**, haga click sobre ***Iniciar sesión*** e ingrese los siguientes datos:

        Nombre de usuario: fernanda
        Contraseña: usertest


        # Para iniciar sesion como usuario:
        Nombre de usuario: manuel
        Contraseña: usertest

    **Para acceder a la página administrativa del sitio ingrese a http://127.0.0.1:8000/admin/ con la siguiente información:**

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

