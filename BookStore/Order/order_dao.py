from Order.order import Order
import joblib

class OrderDAO:
    ORDER_DB_FILE = 'orderDB.pkl'
    
    def __init__(self):
        self.__load_orderDB()

    def __load_orderDB(self):
        try:
            self.__orderDB - joblib.load(OrderDAO.ORDER_DB_FILE)
        except Exception:
            self.__orderDB = {}
    
    def save_orderDB(self):
        if self.__orderDB:
            joblib.dump(self.__orderDB, OrderDAO.ORDER_DB_FILE)

    #주문 추가
    def insert_order(self, order):
        order.set_order_no(self.__next_no())
        self.__orderDB[order.get_order_no()] = order
        self.save_orderDB()
        return order.get_order_no()
    # 주문 존재 확인
    def is_order_exist(self, order_no):
        if order_no in self.__orderDB.keys():
            return True
        return False
    #주문 목록(관리자용)
    def select_all_orders(self, member_id = None):
        if not self.__orderDB:
            return []
        orders = list(self.__orderDB.values())
        if member_id is None:
            return orders
        return [o for o in orders if o.get_member_id() == member_id]
    #주문 단건 조회
    def select_order(self, order_no):
        if self.is_order_exist(order_no):
            self.__orderDB.pop(order_no)
            self.save_orderDB()
            return True
        return False
    #주문 삭제
    def delete_order(self, order_no):
        if self.is_order_exist(order_no):
            self.__orderDB.pop(order_no)
            self.save_orderDB()
            return True
        return False
    
if __name__ == '__main__':
    from datetime import datetime
    dao = OrderDAO()