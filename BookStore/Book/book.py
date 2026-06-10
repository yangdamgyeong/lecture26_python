class Book:
    def __init__(self, book_no, title, author, publisher, price, stock):
        self.__book_no = book_no
        self.__title = title
        self.__author = author
        self.__publisher = publisher
        self.__price = price
        self.__stock = stock

    def get_book_no(self):
        return self.__book_no
    def get_title(self):
        return self.__title
    def get_author(self):
        return self.__author
    def get_publisher(self):
        return self.__publisher
    def get_price(self):
        return self.__price
    def get_stock(self):
        return self.__stock
    
    def __str__(self):
        return (f'[{self.__book_no}] {self.__title} / {self.__author} / 'f'{self.__publisher} / {self.__price:,}원 / 재고 {self.__stock}권')