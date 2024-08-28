# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que la aplicación correrá
EXPOSE 5004  
# puerto front

# Comando para ejecutar la aplicación

CMD ["flask", "run", "--host=0.0.0.0", "--port=5004"]
