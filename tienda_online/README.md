# Tunto Online — Django + React

Proyecto full stack para la práctica RA2. El backend conserva el catálogo de la Unidad 1 e incorpora usuarios con correo, CRUD administrativo protegido, JWT y datos personales. El frontend en React ofrece registro, login, sesión persistente, un dashboard protegido y consumo de la API externa Dog CEO y del servicio SOAP.

## Requisitos

- Python 3.11 o posterior
- Node.js 20 o posterior y npm
- Acceso a Internet para consultar Dog CEO y el servicio SOAP público

## Iniciar el backend

Desde la carpeta `tienda_online/`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

El API queda en `http://127.0.0.1:8000/`; Swagger en `/swagger/` y Django Admin en `/admin/`. Si el proyecto ya tenía una base migrada con el usuario personalizado, basta instalar la dependencia Zeep y ejecutar el servidor. Si la base fue migrada previamente con `auth.User`, véase la nota de abajo antes de recrearla.

## Iniciar React

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite abre el frontend en `http://127.0.0.1:5173/` y redirige `/api` y `/swagger` al backend local. Crea una cuenta en `/registro/` (o ruta `/registro`) y entra con su correo y contraseña.

## Endpoints principales

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/api/auth/register/` | Registro público de cuenta |
| `POST` | `/api/auth/token/` | Access y refresh token con email/contraseña |
| `POST` | `/api/auth/token/refresh/` | Renovar access token |
| `GET` | `/api/auth/me/` | Perfil propio (requiere Bearer JWT) |
| `GET/POST` | `/api/users/` | Leer/crear usuarios (solo admin) |
| `GET/PUT/PATCH/DELETE` | `/api/users/{id}/` | Administrar usuario (solo admin) |
| `GET` | `/api/soap/countries/` | Países desde el servicio SOAP público, consumido con Zeep |
| `GET` | `/swagger/` | Documentación interactiva |
| `GET` | `/api/products/`, `/api/categories/` | CRUD del catálogo existente, protegido con JWT |

El dashboard consume la API externa gratuita `https://dog.ceo/api/breeds/image/random` para cargar una imagen aleatoria de un perro.

## Seguridad y configuración

- El usuario personalizado inicia sesión con email e incluye `phone`, visible en Admin y en el serializer/documentación Swagger.
- El serializer declara `password` como `write_only`: el hash no aparece en respuestas de la colección, detalle ni `/auth/me/`.
- El cambio de contraseña es opcional en actualizaciones. Si el campo se omite, el hash actual se conserva; si se envía, Django guarda el nuevo hash con `set_password`.
- El CRUD de usuarios exige permisos de administrador; la creación pública solo está disponible a través del serializer de registro.
- `SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']` configura access tokens de 30 minutos. El frontend guarda el token en `localStorage` para persistir la sesión; la consola registra el access token tras el login para la evidencia de esta práctica. No usar esta demostración de consola en un entorno de producción.
- La llamada SOAP usa `zeep` con timeout HTTP y una caché de una hora. Si el servicio SOAP público no está disponible temporalmente, el endpoint devuelve HTTP 502 y un mensaje de error.
- SQLite (`db.sqlite3`), entornos virtuales, archivos `.env`, bytecode y `node_modules` están excluidos por `.gitignore`.

Para usar un backend con otro puerto en desarrollo, define `VITE_BACKEND_URL` en `frontend/.env.local`, por ejemplo `VITE_BACKEND_URL=http://127.0.0.1:8767`. El valor predeterminado coincide con `runserver` (`http://127.0.0.1:8000`).

## Usuario personalizado y migraciones

`AUTH_USER_MODEL = 'users.User'` debe existir antes de la primera migración de una base nueva. En una instalación limpia, los pasos `migrate` anteriores crean el esquema correcto. No se recomienda cambiar el usuario de autenticación de una base ya migrada a `auth.User`; conserva la base original y prepara una base nueva para esta práctica.

## Repositorio

[GitHub — tinda_online](https://github.com/GeorgieRe2rn/tinda_online)
