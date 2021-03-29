from flask import Blueprint
from .models import Commissions, OrderLines, Orders, ProductPromotions, Products, Promotions
from flask import request
import datetime
from sqlalchemy.sql.expression import cast
import sqlalchemy
from sqlalchemy import func
from statistics import mean
from flask import jsonify

app_bp = Blueprint('app', __name__)

@app_bp.route('/api/v1/orders_data_by_date', methods=['GET'])
def orders_data_by_date():
    """Gathering required order data by date    
    e.g.: GET /orders_data_by_date"""

    if 'date' in request.args:
        date = request.args['date']
        try:
            date_time_obj = datetime.datetime.strptime(date, '%Y%m%d')
        except Exception:
            return "Error: Please specify a date in yyyymmdd format e.g. 20210329, your input was: %s" % date
    else:
        return "Error: No date field provided. Please specify a date in yyyymmdd format e.g. 202103289"

    total_quanity_sold_on_date = number_of_unique_customers_on_date = total_amount_of_discounts_on_date = order_total_avg_on_date = discount_rate_avg_on_date = total_commissions_amount_on_date = order_avg_commissions_on_date = 0
    commissions_per_promotion = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}

    orders_on_date = Orders.query.filter(func.DATE(Orders.created_at) == date_time_obj.date()).all()
    if orders_on_date:
        order_lines_on_date =  OrderLines.query.with_entities(OrderLines.quantity, OrderLines.discounted_amount, OrderLines.discount_rate, 
                                                            OrderLines.total_amount, OrderLines.order_id, OrderLines.product_id).filter(OrderLines.order_id.in_((order.id for order in orders_on_date))).all()
        total_quanity_sold_on_date = sum((row[0] for row in order_lines_on_date))
        number_of_unique_customers_on_date = len(set([order.customer_id for order in orders_on_date]))
        total_amount_of_discounts_on_date = round(sum((row[1] for row in order_lines_on_date)), 2)
        discount_rate_avg_on_date = round(mean((row[2] for row in order_lines_on_date)), 2)
        order_total_avg_on_date = round(mean((row[3] for row in order_lines_on_date)), 2)
        commissions_rates_on_date = dict(Commissions.query.with_entities(Commissions.vendor_id, Commissions.rate).filter(func.DATE(Commissions.date) == date_time_obj.date()).all())
        promotions_on_date = dict(ProductPromotions.query.with_entities(ProductPromotions.product_id, ProductPromotions.promotion_id).filter(func.DATE(ProductPromotions.date) == date_time_obj.date()).all())

        #logic to calculate commissions, assuming that commission for order is total_amount * vendors commission rate
        
        for row in order_lines_on_date:
            order_id = row[4]
            vendor_id = [order.vendor_id for order in orders_on_date if order.id==order_id][0]
            product_id = row[5]
            commission_rate_for_vendor = commissions_rates_on_date.get(vendor_id)
            commission_for_order_line = commission_rate_for_vendor * row[3]
            total_commissions_amount_on_date =+ round(commission_for_order_line, 2)

            if promotions_on_date.get(product_id):
                commissions_per_promotion[str(promotions_on_date.get(product_id))] =+ round(commission_for_order_line, 2)

        order_avg_commissions_on_date = round(total_commissions_amount_on_date/len(orders_on_date), 2)

    return jsonify(
        customers=number_of_unique_customers_on_date,
        total_discount_amount=total_amount_of_discounts_on_date,
        items=total_quanity_sold_on_date,
        order_total_avg=order_total_avg_on_date,
        discount_rate_avg=discount_rate_avg_on_date,
        commissions={"promotions": commissions_per_promotion,
                     "total": total_commissions_amount_on_date,
                     "order_average": order_avg_commissions_on_date}
    )