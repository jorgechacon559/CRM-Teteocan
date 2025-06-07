# CRM Teteocan – Gestión de Organizaciones y Desarrollo Comercial

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Migraciones y base de datos](#migraciones-y-base-de-datos)
- [Ejecución](#ejecución)
- [Funcionalidades](#funcionalidades)
- [Endpoints principales](#endpoints-principales)
- [Seguridad y roles](#seguridad-y-roles)
- [Gestión de usuarios](#gestión-de-usuarios)
- [Frontend: UX y notificaciones](#frontend-ux-y-notificaciones)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Créditos y licencia](#créditos-y-licencia)

---

## Descripción general

**CRM de Desarrollo Comercial Teteocan** es una plataforma moderna para la gestión de organizaciones y el seguimiento comercial, diseñada para equipos de ventas y agentes que buscan optimizar la prospección, el contacto y la conversión de empresas y negocios locales en clientes.  
El sistema permite registrar organizaciones, asignar agentes, realizar seguimientos, gestionar el estado de cada organización (prospecto, cliente, descartado) y visualizar métricas clave, todo con una experiencia de usuario mejorada y una interfaz atractiva.

---

## Requisitos

- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- npm/yarn

---

## Instalación

### Backend

1. Clona el repositorio y entra al directorio del backend:

    ```sh
    cd proyecto_back_end
    ```

2. Instala las dependencias de Python:

    ```sh
    pip install -r requirements.txt
    ```

3. Crea la base de datos en MySQL:

    ```sql
    CREATE DATABASE storedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

4. Configura tu archivo `.env` con los datos de conexión:

    ```
    DB_USER=root
    DB_PASSWORD=root
    DB_HOST=localhost
    DB_NAME=storedb
    DB_PORT=3306
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

### Frontend

1. Entra al directorio del frontend:

    ```sh
    cd proyecto_front_end
    ```

2. Instala las dependencias de Node.js:

    ```sh
    npm install
    ```

3. Configura el archivo `.env` con la URL del backend:

    ```
    VITE_API_URL=http://localhost:5000/api
    ```

---

## Estructura del proyecto

```
proyecto_back_end/
    app/
        controllers/
        models/
        routes/
        ...
    migrations/
    requirements.txt
    .env
    config.py

proyecto_front_end/
    src/
        components/
        api/
        stores/
        router/
        assets/
        App.vue
        main.js
    public/
    .env
    package.json
    vite.config.js
```

---

## Configuración

- Variables de entorno para backend y frontend.
- Configuración de CORS y JWT.
- Personalización de puertos y rutas según entorno.

---

## Migraciones y base de datos

Inicializa y ejecuta las migraciones para crear las tablas:

```sh
flask db init
flask db migrate -m "tablas de organizaciones y seguimientos"
flask db upgrade
```

---

## Ejecución

### Backend

```sh
flask run
```

### Frontend

```sh
npm run dev
```

---

## Funcionalidades

### Backend

- 🔐 **Autenticación JWT:** Registro, login, refresh y logout seguro.
- 👤 **Gestión de usuarios y roles:** Soporte para roles `admin` y `agente`. Solo los admins pueden gestionar usuarios.
- 🏢 **Gestión de organizaciones:** CRUD completo de organizaciones, clasificadas como empresas o negocios locales, con campos y detalles específicos según el tipo.
- 📋 **Seguimiento comercial:** Registro y consulta de seguimientos, historial de interacciones, asignación de agentes y control de estados (prospecto, cliente, descartado).
- 📈 **Reportes y métricas:** Endpoints para estadísticas de avance comercial y conversión.
- 🛡️ **Baja lógica y control de acceso:** Usuarios y organizaciones pueden ser dados de baja sin perder historial.

### Frontend

- 🖥️ **Dashboard:** Visualización de métricas y gráficas de avance comercial.
- 🏢 **Gestión de organizaciones:** Alta, edición, búsqueda y filtrado avanzado de empresas y negocios locales.
- 🔄 **Seguimiento y conversión:** Registro de contactos, cambios de estado y visualización de historial de cada organización.
- 👤 **Gestión de usuarios:** Alta, edición, baja lógica y ascenso de rol (admin/agente).
- 🎨 **UI/UX mejorada:** Interfaz moderna, responsiva, con validaciones visuales, modales, toasts personalizados y experiencia de usuario optimizada.
- ✅ **Notificaciones toast:** Mensajes de éxito y error con toasts personalizados (verde para éxito, rojo para errores o bajas).

---

## Endpoints principales

| Método | Ruta                                         | Descripción                                 |
|--------|----------------------------------------------|---------------------------------------------|
| POST   | /api/login                                   | Autenticación de usuario                    |
| POST   | /api/refresh                                 | Refrescar token JWT                         |
| POST   | /api/registrar                               | Registro de usuario (agente)                |
| GET    | /api/usuarios                                | Listar usuarios (solo admin)                |
| PUT    | /api/usuarios/<id>/baja                      | Baja lógica de usuario (admin)              |
| PUT    | /api/usuarios/<id>/hacer-admin               | Ascender usuario a admin (admin)            |
| GET    | /api/organizaciones/                         | Listar organizaciones (con filtros)         |
| POST   | /api/organizaciones/                         | Crear organización                          |
| GET    | /api/organizaciones/<id>                     | Obtener detalles de organización            |
| PUT    | /api/organizaciones/<id>                     | Editar organización                         |
| GET    | /api/seguimientos/organizacion/<id>          | Historial de seguimientos de una organización|
| POST   | /api/seguimientos/registrar                  | Registrar seguimiento                       |
| GET    | /api/reportes/resumen-organizaciones         | Resumen por estado de organización          |
| GET    | /api/reportes/organizaciones-nivel-digital   | Organizaciones por nivel de digitalización  |

---

## Seguridad y roles

- **Contraseñas:** Hasheadas con bcrypt.
- **Roles:**  
  - `admin`: Acceso total a usuarios y organizaciones.
  - `agente`: Acceso solo a sus propias organizaciones asignadas y seguimientos.
- **Protección de rutas:**  
  - Solo admins pueden acceder a `/usuarios` y realizar bajas o ascensos.
  - Validación de rol en backend y frontend.
- **Tokens JWT:**  
  - Acceso y refresh token, guardados en sessionStorage.
  - Middleware para refrescar token automáticamente en frontend.
- **Baja lógica:**  
  - El usuario dado de baja no puede volver a iniciar sesión.
  - El email se modifica para evitar duplicados (`email_baja_<id>`).

---

## Gestión de usuarios

- **Registro:**  
  - Validación de email único.
  - Contraseña fuerte (mínimo 8 caracteres, mayúsculas, minúsculas, número y símbolo).
- **Login:**  
  - Devuelve datos completos del usuario (incluyendo email y rol).
- **Ascenso a admin:**  
  - Modal de confirmación, requiere contraseña del admin actual.
  - Toast verde al éxito, mensaje de error si la contraseña es incorrecta.
- **Baja lógica:**  
  - Solo admins pueden dar de baja.
  - Toast rojo al dar de baja, mensaje de error si falla.

---

## Frontend: UX y notificaciones

- **Toasts personalizados:**  
  - Componente reutilizable.
  - Verde para éxito (`success`), rojo para errores o bajas (`error`).
  - Cierre automático y manual.
- **Validaciones visuales:**  
  - Inputs con feedback visual para errores.
  - Mensajes claros en formularios de login, registro y CRUD de organizaciones.
- **Paginación y búsqueda:**  
  - Listados paginados y filtrados de organizaciones y usuarios.
- **Modal de ascenso:**  
  - Confirmación con contraseña antes de ascender a admin.
- **Diseño moderno y responsivo:**  
  - Mejoras visuales y de experiencia en todos los módulos.

---

## Pruebas

- Pruebas unitarias y de integración en `tests/` (backend).
- Scripts de test para frontend (`npm test` o `yarn test`).

---

## Despliegue

- Uso de variables de entorno (.env)
- Soporte para Gunicorn y Nginx (opcional)
- Hosting sugerido: Render, Heroku, DigitalOcean, Vercel (frontend)
- Configuración de Docker (opcional)

---

## Créditos y licencia

**Autores:**  
Quasar y Pulsar

**Año:** 2025  
**Licencia:** MIT / GPL / Privado

---