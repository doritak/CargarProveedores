# Usa una imagen base oficial de Python
FROM python:3.12

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto para Django (opcional si usás gunicorn/uwsgi)
EXPOSE 8000

# Comando para correr el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]