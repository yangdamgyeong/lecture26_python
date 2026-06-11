from Order.order_dao import OrderDAO
from Order.order_item_dao import OrderItemDAO
from Order.order import Order
from Order.order_item import OrderItem
from Cart.cart_dao import CartDAO

class OrderService:
    def __init__(self, orderDAO, orderItemDAO, cartDAO):
        self.__order_dao = orderDAO
        self.__order_item_dao = orderItemDAO
        self.__cart_dao = cartDAO

    def add_order(self, order):
        # 주문 등록 후 부여된 주문번호 반환
        return self.__order_dao.insert_order(order)
    
    def get_order_info(self, member_id = None):
        # member_id 없으면 전체 주문(관리자용)
        return self.__order_dao.select_all_orders(member_id)
    
    def get_order(self, order_no):
        return self.__order_dao.select_order(order_no)
    
    def add_order_item(self, order_no, book_no, count, price):
        self.__order_item_dao.insert_order_item(OrderItem(order_no, book_no, count, price))
        return True
    
    def get_order_item(self, order_no):
        return self.__order_item_dao.delete_order_item(order_no)
    
    def cancel_order(self, order_no):
        # 주문 취소 : 주문 + 주문항목 함께 제거
        self.__order_item_dao.delete_order_item(order_no)
        return self.__order_dao.delete_order(order_no)
    
if __name__ == '__main__':
    from datetime import datetime
    osv = OrderService(OrderDAO(), OrderItemDAO(), CartDAO())