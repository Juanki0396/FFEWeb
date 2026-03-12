# FFEWeb — Plataforma de Gestión de Formación en Empresa

Aplicación web para la gestión integral del proceso de Formación en Empresa (FFE) del Grado Superior de Desarrollo de Aplicaciones Web (DAW), desarrollada con Django.

> Proyecto en desarrollo activo. Este README refleja el estado y la planificación actual.

---

## Descripción

FFEWeb pone en contacto a los cuatro actores del proceso de prácticas:

- **Alumnos** — consultan ofertas, aplican a empresas y hacen seguimiento de su proceso
- **Tutores** — supervisan las candidaturas de sus alumnos, validan ofertas y gestionan la documentación oficial
- **Tutores de empresa** — publican ofertas, gestionan candidatos y colaboran en la elaboración del plan de formación
- **Institutos** — gestionan a sus tutores, ciclos formativos y participan en la firma de la documentación oficial

La aplicación cubre el ciclo completo: desde la publicación de una oferta hasta la tramitación de toda la documentación necesaria para oficializar el puesto de prácticas.

El acceso a la plataforma está controlado por un sistema de invitaciones: el administrador invita a los institutos, los institutos invitan a sus tutores, y los tutores o alumnos pueden invitar a empresas. Esto permite también gestionar procesos de selección privados cuando un alumno ya tiene las prácticas acordadas de antemano.

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
├── accounts/           # Usuarios, roles, perfiles y sistema de invitaciones
├── institutos/         # Institutos, ciclos formativos y oferta educativa
├── empresas/           # Empresas, representantes legales y tutores de empresa
├── ofertas/            # Publicación y gestión de ofertas de prácticas
├── candidaturas/       # Proceso de selección de candidatos
├── documentacion/      # Plan de formación, convenios y documentación oficial
├── templates/          # Templates HTML globales
├── static/             # Archivos estáticos
├── manage.py
└── pyproject.toml
```

### Apps y responsabilidades

**`accounts`** — Autenticación y perfiles de usuario. Modelo `Usuario` personalizado (hereda de `AbstractUser`) con login por email y campo `rol` (alumno / tutor / tutor_empresa / instituto). Perfiles por rol: `PerfilAlumno` y `PerfilTutor`. Incluye el sistema de invitaciones para el registro controlado de usuarios.

**`institutos`** — Catálogo de ciclos formativos y modalidades, gestión de institutos y su relación con los ciclos que imparten (`InstitutoCiclo`). Modelos `CursoAcademico` y `OfertaEducativa` para la dimensión temporal del proceso.

**`empresas`** — Entidad `Empresa` con sus datos jurídicos y representante legal para la documentación oficial. `TutorEmpresa` es el usuario activo de la empresa en la plataforma, pudiendo haber varios por empresa.

**`ofertas`** — CRUD de ofertas por parte de los tutores de empresa. Incluye revisión y validación por el tutor docente antes de la publicación, y un catálogo de búsqueda para alumnos.

**`candidaturas`** — Flujo de aplicación del alumno a una oferta (pública o privada), gestión del estado del proceso por la empresa y seguimiento global por el tutor.

**`documentacion`** — Generación y gestión del plan de formación (asignaturas, Resultados de Aprendizaje y porcentajes), convenio de prácticas, seguimiento y evaluación final. Se activa una vez la empresa ha seleccionado a un candidato.

---

## Modelo de datos destacado

### Usuario y perfiles

```
Usuario (AbstractUser)
  ├── email               → campo de login (único)
  ├── rol                 → alumno | tutor | tutor_empresa | instituto
  └── email_verified      → preparado para verificación futura

  ├── PerfilAlumno        → nif (único), fecha_nacimiento, FK a OfertaEducativa
  └── PerfilTutor         → telefono, FK a OfertaEducativa
```

### Institutos y ciclos

```
CicloFormativo          → nombre, codigo
InstitutoCiclo          → FK Instituto, FK CicloFormativo, modalidad
CursoAcademico          → ano_inicio, ano_fin
OfertaEducativa         → FK InstitutoCiclo, FK CursoAcademico

Instituto               → nombre, codigo, direccion, OneToOne Usuario
```

### Empresas

```
Empresa                 → nombre, cif, direccion, actividad, ...
RepresentanteLegal      → nif, nombre, cargo, FK Empresa
TutorEmpresa (perfil)   → cargo, telefono, FK Empresa, OneToOne Usuario
```

### Plan de formación

```
PlanFormacion           → FK alumno, FK empresa, FK tutor
    └── (M2M through RAEnEmpresa)
            ├── resultado_aprendizaje
            └── porcentaje
```

---

## Instalación y arranque en desarrollo

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd FFEWeb

# Instalar dependencias
uv sync

# Aplicar migraciones
uv run python manage.py migrate

# Crear superusuario
uv run python manage.py createsuperuser

# Arrancar servidor de desarrollo
uv run python manage.py runserver
```

---

## Licencia

Este proyecto está licenciado bajo la [GNU Affero General Public License v3.0](LICENSE).

Cualquier despliegue público de este software, incluso como servicio web sin distribución de binarios, obliga a publicar el código fuente de las modificaciones bajo la misma licencia.
