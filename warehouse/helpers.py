from .extensions import mongo

def prepare_product(product):
    if '_id' in product:
        product['_id'] = str(product['_id'])
    result = mongo.db.stock_changes.aggregate([
        { '$match': {'product_id': product['_id']} },
        { '$group': { '_id': '$product_id', 'total': { '$sum': '$amount' } } }
    ])
    result = list(result)
    amount = 0
    if result:
        amount = result[0]['total']
    product['amount'] = amount
    return product
