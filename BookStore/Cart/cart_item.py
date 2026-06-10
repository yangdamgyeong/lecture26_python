class CartItem:
    def __init__(self, member_id, book_no, count):
        self.__member_id = member_id
        self.__book_no = book_no
        self.__count = count
    
    def get_member_id(self):
        return self.__member_id
    def get_book_no(self):
        return self.__book_no
    def get_count(self):
        return self.__count
    
    def __str__(self):
        return f'도서번호 {self.__book_no}\t수량 {self.__count}'