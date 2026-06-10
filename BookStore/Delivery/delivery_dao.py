from Delivery.delivery import Delivery
import joblib

class DeliveryDAO:
    BOOK_DB_FILE = 'deliveryDB.pkl'
    def __init__(self):
        self.__load_deliveryDB()

    def __load_deliveryDB(self):
        try:
            self.__deliveryDB = joblib.load(DeliveryDAO.DELIVERY_Db_FILE)
        except Exception:
            self.__deliveryDB = {}
    
    def save_deliveryDB(self):
        if self.__deliveryDB:
            joblib.dump(self.__deliveryDB, DeliveryDAO.DELIVERY_Db_FILE)

    # 배송 정보 추가
    def insert_delivery(self, delivery):
        self.__deliveryDB[delivery.get_delivery_no()] = delivery
        self.save_deliveryDB()
        return delivery.get_delivery_no()
    #배송 존재 확인
    def is_delivery_exist(self, delivery_no):
        if delivery_no in self.__deliveryDB.keys():
            return True
        return False
    #주문 번호로 배송 조회
    def select_delivery_by_order(self, order_no):
        for delivery in self.__deliveryDB.values():
            if delivery.get_order_no() == order_no:
                return delivery
        return None
    #전체 배송 목록(관리자)
    def select_all_deliveries_admin(self):
        if self.__deliveryDB:
            return list(self.__deliveryDB.values())
        return[]
    # 배송 상태 변경
    def update_delivery_status(self, delivery_no, status):
        if self.is_delivery_exist(delivery_no):
            self.__deliveryDB[delivery_no].set_delivery_status(status)
            self.save_deliveryDB()
            return True
        return False
    #배송 삭제
    def delete_delivery(self, delivery_no):
        if self.is_delivery_exist(delivery_no):
            self.__deliveryDB.pop(delivery_no)
            self.save_deliveryDB()
            return True
        return False
    
if __name__ == '__main__':
    dao = DeliveryDAO()