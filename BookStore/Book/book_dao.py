from Book.book import Book
import joblib

class BookDAO:
    BOOK_DB_FILE = 'bookDB.pkl'

    def __init__(self):
        self.__book_seq = 0
        self.__bookDB = {}
        self.__load_bookDB()

    def __load_bookDB(self):
        try:
            self.__bookDB = joblib.load(BookDAO.BOOK_DB_FILE)
            if self.__bookDB:
                self.__book_seq = max(self.__bookDB.keys())
        except Exception:
            self.__bookDB = {}
    
    def save_bookDB(self):
        if self.__bookDB:
            joblib.dump(self.__bookDB, BookDAO.BOOK_DB_FILE)

            
    #도서 신규 등록
    def insert_book(self, book):
        self.__book_seq += 1
        book.set_book_no(self.__book_seq)
        self.__bookDB[self.__book_seq] = book
        self.save_bookDB()
        return True
    
    #동일 도서 존재 확인
    def is_book_exist(self, book_no):
        if book_no in self.__bookDB.keys():
            return True
        return False
    #도서 목록
    def select_all_book(self):
        return list(self.__bookDB.values())
    #도서 상세
    def select_book_info(self, book_no):
        if self.is_book_exist(book_no):
            return self.__bookDB[book_no]
        else:
            return None
    #도서 정보/재고 수정
    def update_book(self, book_no, book):
        if self.is_book_exist(book_no):
            book.set_book_no(book_no)
            self.__bookDB[book_no] = book
            self.save_bookDB()
            return True
        return False
    #도서 삭제
    def delete_book(self, book_no):
        if self.is_book_exist(book_no):
            self.__bookDB.pop(book_no)
            self.save_bookDB()
            return True
        return False
    
if __name__ == '__main__':
    dao = BookDAO()