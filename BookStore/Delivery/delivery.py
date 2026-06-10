class Delivery:

    READY = '배송준비'
    SHIPPING = '배송중'
    DONE = '배송완료'
    CANCELED = '배송취소'
    RETURNED = '반품회수'

    def __init__(self, delivery_no, order_no, delivery_address, delivery_status=READY):
        self.__delivery_no = delivery_no
        self.___order_no = order_no
        self.__delivery_address = delivery_address
        self.__delivery_status = delivery_status

    def get_delivery_no(self):
        return self.__delivery_no
    def get_order_no(self):
        return self.___order_no
    def get_delivery_address(self):
        return self.__delivery_address
    def get_delivery_status(self):
        return self.__delivery_status
    def set_delivery_no(self):
        self.__delivery_no
    def set_delivery_status(self):
        self.__delivery_status
    
    def __str__(self):
        return (f'배송번호 {self.__delivery_no}\t주문번호 {self.__order_no}\t'f'{self.__delivery_address}\t[{self.__delivery_status}]')