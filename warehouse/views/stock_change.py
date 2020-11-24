from bson import json_util
from bson.objectid import ObjectId

from flask.views import MethodView
from flask import request, abort, jsonify

from warehouse.extensions import mongo
from warehouse.blueprints import api
from warehouse.helpers import prepare_product


@api.route('/products/<product_id>/change_quantity', methods=['POST'])
def post(product_id):
	product = mongo.db.products.find_one_or_404({
		'_id': ObjectId(product_id),
	})

	# --- Data validation ---
	if not request.is_json:
		abort(400, description='Request must be in json')

	if 'amount' not in request.json:
		abort(400, description='Request must include the amount')

	amount = request.json['amount']

	if not isinstance(amount, int):
		abort(400, description='amount must be an integer')

	stock_change = mongo.db.stock_changes.insert_one({
		'product_id': product_id,
		'amount': amount,
	})

	return jsonify(prepare_product(product))
