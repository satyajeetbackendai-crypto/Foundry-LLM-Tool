def get_order_status(order_id):
    orders = {
        "ORD101": "Shipped",
        "ORD102": "Delivered",
        "ORD103": "Processing"
    }
    return orders.get(order_id, "Order not found")
