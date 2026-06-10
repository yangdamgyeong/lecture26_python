from Book.book_dao import BookDAO
from Book.book import Book

class BookService:
    def __init__(self, bookDAO):
        self.__dao = bookDAO

    def register_book(self, book):
        return self.__dao.insert_book(book)
    
    def search_book(self, keyword=None):
        book_list = self.__dao.select_all_book()
        if keyword:
            keyword = keyword.lower()
            book_list = [b for b in book_list
                         if keyword in b.get_title().lower()
                         or keyword in b.get_author().lower()]
        return book_list
    
    def get_book_info(self, book_no):
        return self.__dao.select_book_info(book_no)
    
    def update_stock(self, book_no, book):
        return self.__dao.update_book(book_no, book)
    
    def reduce_stock(self, book_no, count):
        book = self.__dao.select_book_info(book_no)
        if not book:
            return False
        if book.get_stock() < count:
            return False
        book.set_stock(book.get_stuck() - count)
        return self.__dao.update_book(book_no, book)
    
    def restore_stock(self, book_no, count):
        book = self.__dao.select_book_info(book_no)
        if not book:
            return False
        book.set_stock(book.get_stock() + count)
        return self.__dao.update_book(book_no, book)
    
    def remove_book(self, book_no):
        return self.__dao.delete_book(book_no)
    
if __name__ == '__main__':
    bsv = BookService(BookDAO())