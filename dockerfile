# Dockerfile

# 1. Usamos una imagen oficial de Python 3.x (slim para reducir tamaño)
FROM python:3.11-slim

# 2. Añadimos metadatos (opcional)
LABEL maintainer="yohperez"
LABEL description="API de recetas con FastAPI, PostgreSQL y Docker."

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos requirements.txt y instalamos dependencias
COPY requirements.txt .

# Instalamos en producción (sin caché extra)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código de la API (app/)
COPY ./app /app/app

# 6. Aseguramos permisos de ejecución del entrypoint (si tuvieras uno)
RUN chmod +x /app/app/main.py

# 7. Exponemos el puerto donde corre FastAPI
EXPOSE 8000

# 8. Comando para arrancar la API con Uvicorn
# Escuchamos en 0.0.0.0 para que el contenedor sea accesible desde fuera
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]