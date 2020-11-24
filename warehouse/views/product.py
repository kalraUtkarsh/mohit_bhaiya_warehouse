'''
GET    /products            List all products
POST   /products            Add a new product
GET    /products/<id>       Get a product by id
PATCH  /products/<id>       Modify a product
DELETE /products/<id>       Delete a product
'''

from bson import json_util
from bson.objectid import ObjectId

from flask.views import MethodView
from flask import request, abort, jsonify

from warehouse.extensions import mongo
from warehouse.blueprints import api
from warehouse.helpers import prepare_product


class ProductsAPI(MethodView):
    def get(self):
        products = mongo.db.products.find()
        products = [prepare_product(product) for product in products]
        return jsonify(products)

    def post(self):
        # --- Data validation ---
        if not request.is_json:
            abort(400, description='Request must be in json')

        if not all(key in request.json for key in ['name', 'manufacturer', 'price']):
            abort(400, description='Request must include the name, manufacturer, and price')

        name = request.json['name']
        manufacturer = request.json['manufacturer']
        price = request.json['price']

        if not isinstance(name, str):
            abort(400, description='name must be a string')
        if not isinstance(manufacturer, str):
            abort(400, description='manufacturer must be a string')
        if not isinstance(price, int):
            abort(400, description='price must be an integer')

        # --- Storing the product ---
        product = {
            'name': name,
            'manufacturer': manufacturer,
            'price': price,
        }
        mongo.db.products.insert_one(product)

        return jsonify(prepare_product(product))

api.add_url_rule('/products',
                 view_func=ProductsAPI.as_view('products_api'),
                 methods=('GET', 'POST'),
                )


class ProductDetailAPI(MethodView):
    def get(self, product_id):
        product = mongo.db.products.find_one_or_404({
            '_id': ObjectId(product_id),
        })
        return jsonify(prepare_product(product))

    def patch(self, product_id):
        product = mongo.db.products.find_one_or_404({
            '_id': ObjectId(product_id),
        })
        # --- Data validation ---
        if not request.is_json:
            abort(400, description='Request must be in json')

        if not any(key in request.json for key in ['name', 'manufacturer', 'price']):
            abort(400, description='Request must include the name, manufacturer, or price')

        name = request.json.get('name', product['name'])
        manufacturer = request.json.get('manufacturer', product['manufacturer'])
        price = request.json.get('price', product['price'])

        if not isinstance(name, str):
            abort(400, description='name must be a string')
        if not isinstance(manufacturer, str):
            abort(400, description='manufacturer must be a string')
        if not isinstance(price, int):
            abort(400, description='price must be an integer')

        product = {
            'name': name,
            'manufacturer': manufacturer,
            'price': price,
        }
        mongo.db.products.update({'_id': ObjectId(product_id)}, product)

        return jsonify(prepare_product(product))

    def delete(self, product_id):
        mongo.db.products.find_one_or_404({
            '_id': ObjectId(product_id),
        })

        result = mongo.db.products.delete_one({
            '_id': ObjectId(product_id),
        })

        mongo.db.stock_changes.delete_many({
            'product_id': product_id,
        })

        return jsonify({
            'success': result.deleted_count == 1,
        })


api.add_url_rule('/products/<product_id>',
                 view_func=ProductDetailAPI.as_view('product_api'),
                 methods=('GET', 'PATCH', 'DELETE'),
                )
