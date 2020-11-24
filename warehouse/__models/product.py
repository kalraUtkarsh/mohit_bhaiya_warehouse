"""Models representing product"""

from warehouse.extensions import db
from .stock_change import StockChange


class Product(db.Model):
    """Represents a product."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_name = db.Column(db.String(128))

    model_name = db.Column(db.String(128))
    price = db.Column(db.Integer)

	@property
    def quantity(self):
        """Return the user's innopoints balance."""
        return db.session.query(
            db.func.sum(StockChange.amount)
        ).filter(
            StockChange.product_id == self.id
        ).scalar() or 0
