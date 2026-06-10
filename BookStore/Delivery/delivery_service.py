from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery import Delivery

class DeliveryService:
    def __init__(self, deliveryDAO):
        self.__dao = deliveryDAO

    def register_delivery_info(self, delivery):
        return self.__dao.insert_delivery(delivery)
    
    def update_delivery_status(self, delivery_no, status):
        return self.__dao.update_delivery_status(delivery_no, status)
    
    def view_delivery_status_by_order(self, order_no):
        return self.__dao.select_delivery_by_order(order_no)
    
    def view_all_deliveries(self):
        return self.__dao.select_all_deliveries_admin()
    
    def remove_delivery(self, delivery_no):
        return self.__dao.delete_delivery(delivery_no)
    
    def cancel_delivery_by_order(self, order_no):
        #주문 취소 시 연결된 배송 제거
        delivery = self.__dao.select_delivery_by_order(order_no)
        if delivery:
            return self.__dao.delete_delivery(delivery.get_delivery_no())
        return False
if __name__ == '__main__':
    dsv = DeliveryService(DeliveryDAO())