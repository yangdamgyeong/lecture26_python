from Order.order_item import OrderItem
import joblib

class OrderItemDAO:
    ORDER_ITEM_DB_FILE = 'orderItemDB.pkl'
    def __init__(self):
        self.__load_orderItemDB()

    def __load_orderItemDB(self):
        try:
            self.__orderItemDB - joblib.load(OrderItemDAO.ORDER_ITEM_DB_FILE)
        except Exception:
            self.__orderItemDB = {}
    
    def save_orderItemDB(self):
        if self.__orderItemDB:
            joblib.dump(self.__orderDB, OrderItemDAO.ORDER_ITEM_DB_FILE)

    # 주문 항목 추가
    def insert_order_item(self, order_item):
        order_no = order_item.get_order_no()
        if order_no not in self.__orderItemDB:
            self.__orderItemDB[order_no] = []
        self.__orderItemDB[order_no].append(order_item)
        self.save_orderItemDB()
    #주문 항목 조회
    def select_order_item_info(self, order_no):
        if order_no in self.__orderItemDB:
            return self.__orderItemDB[order_no]
        return[]
    #주문 항목 존재 확인
    def is_order_item_exist(self, order_no):
        if order_no in self.__orderItemDB.keys():
            return True
        return False
    #주문 항목 삭제
    def delete_order_item(self, order_no):
        if self.is_order_item_exist(order_no):
            self.__orderItemDB.pop(order_no)
            self.save_orderItemDB()
            return True
        return False

if __name__ == '__main__':
    dao = OrderItemDAO()