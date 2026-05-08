# SaborScript API 🍳

API REST para la gestión de recetas de cocina, desarrollada con FastAPI, SQLAlchemy y PostgreSQL (vía Docker).  
Este proyecto corresponde a la asignatura de **desarrollo de un motor de persistencia (backend)**, siguiendo el briefing de proyecto individual.

## 🎯 Objetivo del proyecto

- Implementar un **CRUD completo** de recetas (POST, GET, PUT, DELETE) con persistencia en base de datos.
- Añadir una **relación 1:N** entre `Category` y `Recipe`.
- Incluir **filtros de búsqueda** (por categoría) y documentación automática con Swagger.
- Utilizar **Docker** para contenerizar la API y la base de datos (nivel experto).

## 📂 Estructura del proyecto


```text
api_recetas/
├── app/
│   ├── main.py            # Instancia FastAPI + montaje de routers
│   ├── database.py        # Conexión a la base de datos
│   ├── models.py          # Modelos SQLAlchemy
│   ├── schemas.py         # Modelos Pydantic
│   ├── crud.py            # Funciones CRUD
│   └── routers/
│       └── recipes.py     # Rutas FastAPI de recetas
├── .env.example           # Variables de entorno
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
└── docker-compose.yml```

=======

API REST para gestión de recetas construida con FastAPI y PostgreSQL.

## Instalación
1. Clonar el repo: `git clone www.github.com/yohperez/api_recetas.git `
2. Crear venv: `python -m venv venv`
3. Activar venv y: `pip install -r requirements.txt`
4. Crear archivo `.env` basado en `.env.example`.
5. Ejecutar: `uvicorn app.main:app --reload`

=======
# api_recetas
>>>>>>>

 bba84189f0e0ba2dde83c251516ec4f6bbf53e2b
