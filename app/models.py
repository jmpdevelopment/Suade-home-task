from . import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    vendor_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)

class Commissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    vendor_id = db.Column(db.Integer)
    rate = db.Column(db.Float)

class OrderLines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_description = db.Column(db.Text)
    product_price = db.Column(db.Float)
    product_vat_rate = db.Column(db.Float)
    discount_rate = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    full_price_amount = db.Column(db.Float)
    discounted_amount = db.Column(db.Float)
    vat_amount = db.Column(db.Float)
    total_amount = db.Column(db.Float)

class ProductPromotions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)

class Promotions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)