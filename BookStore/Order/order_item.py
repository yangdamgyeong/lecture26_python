class OrderItem:
    def __init__(self, order_no, book_no, count, price):
        self.order_no = order_no
        self.book_no = book_no
        self.count = count
        self.price = price

    def get_order_no(self):
        return self.__order_no
    def get_book_no(self):
        return self.__book_no
    def get_count(self):
        return self.__count
    def get_price(self):
        return self.__price
    
    def __str__(self):
        return (f'도서번호 {self.__book_no}\t수량 {self.__count}\t'f'단가 {self.__price:,}원\t소계 {self.__price * self.__count:,}원')