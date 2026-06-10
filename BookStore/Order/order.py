class Order:
    def __init__(self, order_no, member_id, total_price, order_date):
        self.__order_no = order_no
        self.__member_id = member_id
        self.__total_price = total_price
        self.__order_date = order_date

    def get_order_no(self):
        return self.__order_no
    def get_member_id(self):
        return self.__member_id
    def get_total_price(self):
        return self.__total_price
    def get_order_date(self):
        return self.__order_date
    
    def __str__(self):
        return (f'주문번호 {self.__order_no}\t{self.__member_id}\t'f'{self.__total_price:,}원\t{self.__order_date}')
