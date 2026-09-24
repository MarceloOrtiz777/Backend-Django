# Sitio Web Modular con Django — Evaluación Sumativa #2

Proyecto desarrollado para la asignatura Programación Back End (TI3041), INACAP La Serena.

Evolución del proyecto de la Evaluación Sumativa #1: se migró la persistencia de datos desde
archivos JSON hacia una base de datos relacional (MySQL/MariaDB) usando Django ORM, se
incorporó Django Admin para la gestión CRUD, y el proyecto está preparado para desplegarse
en una instancia AWS EC2.

## Estructura del proyecto

- **config/** — Proyecto principal Django (settings, urls raíz)
- **inventarioApp/** — App 1: gestión de productos (modelo `Producto`)
- **clientesApp/** — App 2: gestión de clientes y sus pedidos (modelos `Cliente` y `Pedido`,
  relacionado con `Producto` mediante `ForeignKey`)
- **templates/** — Plantillas HTML con herencia (`base.html` + hijas por app)
- **static/** — Bootstrap 5 local, imágenes

## Modelo de datos

```
Producto
├── nombre, categoria, precio, stock, descripcion

Cliente
├── nombre, apellidos, email, telefono, fecha_registro

Pedido
├── cliente   → ForeignKey a Cliente
├── producto  → ForeignKey a Producto
├── cantidad, fecha_pedido
```

## Requisitos

- Python 3.12+
- MySQL 8.4+ o MariaDB 10.5+ (ver nota de compatibilidad más abajo)
- Git

## Instalación local

```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_proyecto>

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # y completa tus datos reales de conexión a la BD
```

Crea la base de datos en MySQL/MariaDB antes de continuar:

```sql
CREATE DATABASE nombre_de_tu_base_de_datos CHARACTER SET utf8mb4;
CREATE USER 'usuario_mysql'@'localhost' IDENTIFIED BY 'password_mysql';
GRANT ALL PRIVILEGES ON nombre_de_tu_base_de_datos.* TO 'usuario_mysql'@'localhost';
FLUSH PRIVILEGES;
```

Luego:

```bash
python manage.py migrate
python manage.py seed_productos     # datos de ejemplo (productos)
python manage.py seed_clientes      # datos de ejemplo (clientes + pedidos)
python manage.py createsuperuser    # para entrar a /admin/
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`.

## ⚠️ Nota de compatibilidad de versión

Django 6.1 requiere **MySQL 8.4+**. Ubuntu 24.04 trae por defecto MySQL 8.0.x vía `apt`,
que **no es compatible**. Alternativas verificadas:

- Instalar MySQL 8.4+ desde el repositorio oficial de Oracle, o
- Usar **MariaDB 10.5+** (probado con 10.11), totalmente compatible con el backend
  `django.db.backends.mysql` gracias al driver `pymysql`.

## Variables de entorno (`.env`)

Ninguna configuración sensible está escrita en el código. Se cargan desde `.env`
(no incluido en el repositorio) mediante `python-decouple`:

```
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=3306
```

Usa `.env.example` como plantilla.

## Django Admin

Todas las entidades (`Producto`, `Cliente`, `Pedido`) están registradas en `admin.py`,
con búsqueda, filtros, y navegación entre relacionadas (los pedidos de un cliente se
pueden crear directamente desde su ficha).

## Estado del frontend

Los listados (`/invent/productos/`, `/clientes/clientes/`) obtienen los datos mediante
Django ORM y muestran botones de Agregar / Modificar / Eliminar / Buscar. Estos botones
son visuales por ahora (marcadores de posición): su funcionalidad completa se implementa
en la siguiente evaluación sumativa.
