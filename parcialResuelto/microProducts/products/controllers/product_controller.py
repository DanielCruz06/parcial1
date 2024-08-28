from flask import Blueprint, request, jsonify
from products.models.products_model import Products
from db.db import db

product_controller = Blueprint('product_controller', __name__)

# Obtener todos los productos
@product_controller.route('/api/products', methods=['GET'])
def get_products():
    print("listado de productos")
    products = Products.query.all()
    result = [{'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products]
    return jsonify(result)

# Obtener un producto por ID
@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    print("obteniendo producto")
    product = Products.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity})

# Crear un nuevo producto
@product_controller.route('/api/products', methods=['POST'])
def create_product():
    print("creando producto")
    data = request.json
    new_product = Products(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Products created successfully'}), 201

# Actualizar un producto existente
@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    print("actualizando producto")
    product = Products.query.get_or_404(product_id)
    data = request.json
    product.name = data['name']
    product.price = data['price']
    product.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Products updated successfully'})

# Eliminar un producto existente
@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Products deleted successfully'})

@product_controller.route('/api/products/<int:product_id>/reduce_stock', methods=['PUT'])
def reduce_stock(product_id):
    """
    Endpoint para reducir el stock de un producto.
    Recibe un JSON con la cantidad a reducir del stock del producto identificado por `product_id`.
    Verifica si hay stock suficiente y realiza la actualización en la base de datos.
    
    Args:
        product_id (int): ID del producto cuyo stock se va a reducir.
    
    Returns:
        JSON: Un mensaje de confirmación si el stock se reduce correctamente,
        o un mensaje de error con el código de estado HTTP apropiado.
    """
    try:
        # Paso 1: Obtener los datos de la solicitud
        data = request.get_json()
        quantity_to_reduce = data.get('quantity')

        # Verificar que la cantidad a reducir sea válida
        if quantity_to_reduce is None or quantity_to_reduce <= 0:
            return jsonify({'message': 'Cantidad a reducir inválida'}), 400

        # Paso 2: Obtener el producto de la base de datos
        product = Products.query.get_or_404(product_id)

        # Paso 3: Verificar si hay suficiente stock
        if product.quantity < quantity_to_reduce:
            return jsonify({'message': 'Stock insuficiente para el producto ID {}'.format(product_id)}), 400

        # Paso 4: Reducir el stock y guardar los cambios
        product.quantity -= quantity_to_reduce
        db.session.commit()

        # Retornar una respuesta de éxito
        return jsonify({'message': 'Stock reducido exitosamente', 'new_stock': product.quantity}), 200
    
    except Exception as e:
        # Manejo de excepciones y rollback en caso de error
        db.session.rollback()
        return jsonify({'message': 'Error al reducir el stock', 'error': str(e)}), 500
