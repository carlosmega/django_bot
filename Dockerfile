
FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo en el contenedor
WORKDIR /app
COPY . .

RUN pip install playwright

RUN playwright install firefox --with-deps
# Copia los archivos de requerimientos y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto en el que la aplicación correrá
EXPOSE 8000

# Comando para correr la aplicación usando xvfb-run
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]