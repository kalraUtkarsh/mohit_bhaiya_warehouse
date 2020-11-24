from flask.views import MethodView
from flask import request, abort, jsonify

from warehouse.extensions import mongo
from warehouse.blueprints import api


@api.route('/products', methods=['POST'])
def add_product():
    # --- Data validation ---
    if not request.is_json():
        abort(400, description='Request must be in json')

    if not all(lambda key: key in request.json, ['name', 'manufacturer', 'price']):
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

    return jsonify(product)


class ProductDetailAPI(MethodView):
    def get(self, product_id: str):
        product = mongo.db.products.find_one_or_404({
            '_id': product_id,
        })
        print(product)
        return product


api.add_url_rule('/products/<int:product_id>',
                 view_func=ProductDetailAPI.as_view('product_api'),
                 methods=('GET',),
                )
