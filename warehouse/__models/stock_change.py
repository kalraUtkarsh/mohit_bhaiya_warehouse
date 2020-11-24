"""Models representing stock changes"""

from warehouse.extensions import db

class StockChange(db.Model):
    """Represents the change in the amount of variety available."""
    __tablename__ = 'stock_changes'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id', ondelete='CASCADE'),
                           nullable=False)
