from flask import Flask
from orders.controllers.order_controller import order_controller
from db.db import db
from flask_cors import CORS

app = Flask(__name__)
#CORS(app, supports_credentials=True)
CORS(app)
# Clave secreta para las sesiones y cookies firmadas
#app.secret_key = 'secret123'

# Carga la configuración de la aplicación desde un objeto de configuración
app.config.from_object('config.Config')
# Inicialización de la base de datos
db.init_app(app)
# Registrando el blueprint del controlador de órdenes
app.register_blueprint(order_controller)
# Configuración de CORS, permitiendo el envío de credenciales
#CORS(app, supports_credentials=True)

# Punto de entrada principal para la aplicación
if __name__ == '__main__':
    app.run()