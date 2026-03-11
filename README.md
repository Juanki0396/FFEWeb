# FFEWeb — Plataforma de Gestión de Formación en Empresa

Aplicación web para la gestión integral del proceso de Formación en Empresa (FFE) del Grado Superior de Desarrollo de Aplicaciones Web (DAW), desarrollada con Django.

> Proyecto en desarrollo activo. Este README refleja el estado y la planificación actual.

---

## Descripción

FFEWeb pone en contacto a los tres actores del proceso de prácticas:

- **Alumnos** — consultan ofertas, aplican a empresas y hacen seguimiento de su proceso
- **Tutores** — supervisan las candidaturas de sus alumnos, validan ofertas y gestionan la documentación oficial
- **Empresas** — publican ofertas, gestionan candidatos y colaboran en la elaboración del plan de formación

La aplicación cubre el ciclo completo: desde la publicación de una oferta hasta la tramitación de toda la documentación necesaria para oficializar el puesto de prácticas.

Aunque el proyecto nace orientado a DAW, la arquitectura está diseñada para soportar otros ciclos formativos en el futuro.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Django 6 |
| Base de datos (desarrollo) | SQLite |
| Base de datos (producción) | PostgreSQL |
| Gestión de dependencias | uv |

---

## Estructura del proyecto

```
FFEWeb/
├── ffeweb/             # Configuración principal del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/           # Usuarios, roles y perfiles
├── ofertas/            # Publicación y gestión de ofertas de prácticas
├── candidaturas/       # Proceso de selección de candidatos
├── documentacion/      # Plan de formación, convenios y documentación oficial
├── templates/          # Templates HTML globales
├── static/             # Archivos estáticos
├── manage.py
└── pyproject.toml
```

### Apps y responsabilidades

**`accounts`** — Autenticación y perfiles de usuario. Modelo `Usuario` personalizado (hereda de `AbstractUser`) con login por email y campo `rol` (alumno / tutor / empresa). Cada rol tiene su propio modelo de perfil: `PerfilAlumno`, `PerfilTutor` y `PerfilEmpresa`.

**`ofertas`** — CRUD de ofertas por parte de las empresas. Incluye revisión y validación por el tutor antes de la publicación, y un catálogo de búsqueda para alumnos.

**`candidaturas`** — Flujo de aplicación del alumno a una oferta, gestión del estado del proceso por la empresa y seguimiento global por el tutor.

**`documentacion`** — Generación y gestión del plan de formación (asignaturas, Resultados de Aprendizaje y porcentajes), convenio de prácticas, seguimiento mensual y evaluación final. Esta app se activa una vez la empresa ha seleccionado a un candidato.

---

## Modelo de datos destacado

### Usuario y perfiles

```
Usuario (AbstractUser)
  ├── email          → campo de login (único)
  ├── rol            → alumno | tutor | empresa
  └── email_verificado → preparado para verificación futura

  ├── PerfilAlumno   → instituto, ciclo_formativo, ...
  ├── PerfilTutor    → departamento, ...
  └── PerfilEmpresa  → nombre, cif, direccion, tutor_empresa, ...
```

---

## Roadmap

### Fase 1 — Configuración del proyecto base
- [x] Inicializar proyecto con `uv` y Django
- [x] Crear apps: `accounts`, `ofertas`, `candidaturas`, `documentacion`
- [ ] Configurar `settings.py`
- [ ] Definir modelo de usuario personalizado
- [ ] Primera migración

### Fase 2 — Autenticación y perfiles
- [ ] Modelo `Usuario` con roles y login por email
- [ ] Perfiles por rol (`PerfilAlumno`, `PerfilTutor`, `PerfilEmpresa`)
- [ ] Registro diferenciado por rol
- [ ] Login / logout / recuperación de contraseña
- [ ] Dashboards básicos por rol
- [ ] Panel de administración Django

### Fase 3 — Gestión de ofertas
- [ ] Modelo `Oferta`
- [ ] CRUD de ofertas para empresas
- [ ] Flujo de revisión y validación por tutor
- [ ] Catálogo de ofertas para alumnos

### Fase 4 — Candidaturas
- [ ] Modelo `Candidatura` con estados
- [ ] Flujo de aplicación del alumno
- [ ] Panel de gestión para empresas
- [ ] Seguimiento para tutores
- [ ] Notificaciones internas

### Fase 5 — Documentación
- [ ] Catálogo de asignaturas y RAs (datos fijos del ciclo)
- [ ] Modelo `PlanFormacion` con RAs y porcentajes
- [ ] Validación: porcentajes suman 100% por asignatura
- [ ] Gestión de convenio y documentos oficiales
- [ ] Generación de PDFs
- [ ] Trazabilidad documental

### Fase 6 — Calidad y despliegue
- [ ] Tests unitarios y de integración
- [ ] Dashboard de estadísticas
- [ ] Revisión de UX y responsive
- [ ] Despliegue en producción
- [ ] Verificación de email (mejora futura)

---

## Instalación y arranque en desarrollo

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd FFEWeb

# Instalar dependencias
uv sync

# Crear el fichero de variables de entorno
cp .env.example .env
# Editar .env con tus valores

# Aplicar migraciones
uv run python manage.py migrate

# Crear superusuario
uv run python manage.py createsuperuser

# Arrancar servidor de desarrollo
uv run python manage.py runserver
```

---

