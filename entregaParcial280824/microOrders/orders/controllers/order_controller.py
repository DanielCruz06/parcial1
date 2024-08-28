from flask import Blueprint, request, jsonify, session
from orders.models.order_model import Orders
from db.db import db
import datetime
import requests

order_controller = Blueprint('orders_controller',__name__)

@order_controller.route('/api/orders',methods=['GET'])
def get_all_orders():
    #Obtener todas las ordenes de la base de datos
    orders = Orders.query.all()
    result =  [{'id': order.id, 'userName': order.userName, 'userEmail': order.userEmail, 'saleTotal' : order.saleTotal,
                'date' : order.date} for order in orders]
    print(result)
    return jsonify(result)

@order_controller.route('/api/orders/<int:order_id>',methods=['GET'])
def get_order(order_id):
    #obtener una orden por ID
    order = Orders.query.get_or_404(order_id)
    result =  ({'id': order.id, 'userName': order.userName, 'userEmail': order.userEmail, 'saleTotal' : order.saleTotal,
                'date' : order.date})
    

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    """
    Endpoint para crear una nueva orden.
    Recibe un JSON con una lista de productos con sus respectivos IDs y cantidades.
    Toma la información de usuario desde sesión.
    Calcula el total de la venta, verifica la disponibilidad de los productos y
    actualiza el inventario llamando al endpoint de actualización de productos.
    """
    data = request.get_json()
    print("En orders session actual", session)
    #valia info user
    user_data = data.get('user')
    user_name =user_data.get('name')
    if not user_data:
        return jsonify({'message': 'Falta información del'}), 400

    user_response = requests.get(f"http://192.168.80.3:5002/api/users/{user_name}")
    if user_response.status_code != 200:
        print('bad')
        return jsonify({'message': f"Error al obtener el usuario con username {user_name}"}), user_response.status_code
    user_data_json= user_response.json()
    user_name=user_data_json['username']
    user_email = user_data_json['email']


   # user_name = session.get('username')
   # user_email = session.get('email')
   # user_name = session['username']
   # user_email = session['email']

    if not user_name or not user_email:
        return jsonify({'message': 'Información de usuario inválida'}), 400

    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400

    # Inicializar el total de la venta
    sale_total = 0

    # Verificar disponibilidad de productos y calcular el total
    for product in products:
        product_id = product.get('id')
        quantity = product.get('quantity')

        if not product_id or not quantity or quantity <= 0:
            return jsonify({'message': f'Producto o cantidad inválida: {product}'}), 400

        # Supongamos que llamamos a un endpoint para verificar la disponibilidad del producto y su precio
        product_response = requests.get(f"http://192.168.80.3:5003/api/products/{product_id}")
        if product_response.status_code != 200:
            return jsonify({'message': f'Error al obtener el producto con ID {product_id}'}), product_response.status_code
        
        product_data = product_response.json()
        if product_data['quantity'] < quantity:
            return jsonify({'message': f'Stock insuficiente para el producto ID {product_id}'}), 400

        # Sumar al total de la venta
        sale_total += product_data['price'] * quantity

    # Actualizar el inventario (llamando al endpoint de actualización de Productos)
    for product in products:
        product_id = product.get('id')
        quantity = product.get('quantity')

        # Llamar al servicio de inventario para reducir el stock
        update_response = requests.put(f"http://192.168.80.3:5003/api/products/{product_id}/reduce_stock",
                                       json={'quantity': quantity})
        if update_response.status_code != 200:
            return jsonify({'message': f'Error al actualizar el inventario para el producto ID {product_id}'}), update_response.status_code

    # Crear una nueva instancia de Order y guardarla en la base de datos
    new_order = Orders(
        userName=user_name,
        userEmail=user_email,
        saleTotal=sale_total,
        date=datetime.datetime.now()
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Orden creada exitosamente', 'order_id': new_order.id}), 201
