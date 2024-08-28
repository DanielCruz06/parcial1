# Usa una imagen base de Python
FROM python:3

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias de la aplicación
#RUN pip install mysql

#RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Expone el puerto en el que la aplicación correrá
EXPOSE 5001  
# puerto front

# Comando para ejecutar la aplicación
#CMD ["flask", "run.py", "--host=0.0.0.0", "--port=5001"]
#CMD  ["python","-m","flask", "run.py"]
CMD ["python","run.py"]

