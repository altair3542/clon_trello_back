# Clon de Trello - Backend (Django + DRF + JWT)

Este proyecto es un **MVP** (Producto Mínimo Viable) de un clon de Trello construido con **Django**, **Django REST Framework** y autenticación mediante **JWT**. La idea principal es contar con una API robusta que permita la gestión de usuarios, tableros, listas y tarjetas, sirviendo de base para un frontend moderno (ej. React + Vite + Tailwind).

## Características Principales

- **Autenticación con JWT**: Registro de usuarios, login y obtención de tokens de acceso y refresco.
- **Usuarios**: Creación, gestión del perfil del usuario autenticado.
- **Tableros (Boards)**: Un usuario puede crear tableros, agregarse como miembro, y eventualmente compartirlos con otros usuarios.
- **Listas (Lists)**: Cada tablero puede tener múltiples listas, ordenadas por posición.
- **Tarjetas (Cards)**: Cada lista contiene tarjetas con un título, descripción y una posición.
- **Permisos y Roles básicos**: Solo los miembros de un board pueden ver y gestionar sus listas y tarjetas.
- **Respuestas en JSON** y estilo REST siguiendo las convenciones de DRF.
- **Tests básicos** para asegurar la calidad del código y la lógica de negocio.

## Tecnologías

- **Backend**: Python 3, Django, Django REST Framework
- **Autenticación**: djangorestframework-simplejwt (JWT)
- **Base de Datos**: SQLite (por defecto; puedes cambiar a PostgreSQL u otra)
- **Tests**: Tests integrados con `unittest` y las herramientas nativas de Django + DRF

## Requisitos Previos

- **Python 3.9+** (idealmente)
- Pipenv o venv (opcional, pero recomendado)
- Git (opcional)

## Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/clon-trello-back.git
   cd clon-trello-back

   
2. **Crear y activar entorno virtual (opcional)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   # venv\Scripts\activate    # Windows

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   
    - Si no tienes requirements.txt, puedes crearlo con:
     ```bash
     pip install -r requirements.txt
  Dependencias esenciales:

  - Django
  - djangorestframework
  - djangorestframework-simplejwt
  - drf-nested-routers (opcional, aunque se ha usado en todo el proyecto)    

4. **Migrar la base de datos**:
   ```bash
    python manage.py migrate

5. **Crear un superusuario (opcional)**:
   ```bash
    python manage.py createsuperuser

6. **Iniciar el servidor de desarrollo**:
   ```bash
    python manage.py runserver


- El servidor estará disponible en http://127.0.0.1:8000/

## Endpoints Principales:
- Autenticación:

  - POST /api/users/register/ - Registro de usuario
  - POST /api/token/ - Obtención de tokens (access, refresh)
  - POST /api/token/refresh/ - Refrescar token de acceso
 
- Usuarios:
  
  - GET /api/users/me/ - Perfil del usuario autenticado
  - PATCH /api/users/me/ - Actualizar perfil
 
- Boards:

  - GET /api/boards/ - Listar boards del usuario
  - POST /api/boards/ - Crear board
  - GET /api/boards/{id}/ - Detalle board
  - PATCH /api/boards/{id}/ - Actualizar board
  - DELETE /api/boards/{id}/ - Eliminar board
  
- Lists (dentro de Boards):
  
  - GET /api/boards/{board_id}/lists/
  - POST /api/boards/{board_id}/lists/
  - GET /api/boards/{board_id}/lists/{id}/
  - PATCH /api/boards/{board_id}/lists/{id}/
  - DELETE /api/boards/{board_id}/lists/{id}/

- Cards (dentro de Lists):

  - GET /api/boards/{board_id}/lists/{list_id}/cards/
  - POST /api/boards/{board_id}/lists/{list_id}/cards/
  - GET /api/boards/{board_id}/lists/{list_id}/cards/{id}/
  - PATCH /api/boards/{board_id}/lists/{list_id}/cards/{id}/
  - DELETE /api/boards/{board_id}/lists/{list_id}/cards/{id}/
    
Nota: Excepto en registro y obtención de token, se requiere Authorization: Bearer <token>.


## Permisos y autorizacion:

- Solo miembros de un board pueden ver y editar sus listas y tarjetas.
- Al crear un board, el usuario creador es el owner y miembro inicial.
- Para acceder a boards, listas o tarjetas, el usuario debe ser miembro del board.

## Tests 
- **Ejecuta los test**:
   ```bash
    python manage.py test


## Próximos Pasos
  - Funcionalidades adicionales: Comentarios, etiquetas, asignación de usuarios a tarjetas.
  - Roles avanzados: Distinguir entre owner y miembros, permisos granulares.
  - Frontend: Consumir esta API desde un frontend (ej. React + Vite + Tailwind).
  - Despliegue: Ajustar para entorno de producción, servidores WSGI, etc.


## Contribución
  - Forks, issues y pull requests son bienvenidos.

