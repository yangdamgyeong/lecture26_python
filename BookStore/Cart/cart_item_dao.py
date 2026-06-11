from Cart.cart_item import CartItem
import joblib

class CartItemDAO:
    CART_ITEM_DB_FILE = 'cartItemDB.pkl'
    def __init__(self):
        self.__load_cartItemDB()

    def __load_cartItemDB(self):
        try:
            self.__cartItemDB = joblib.load(CartItemDAO.CART_ITEM_Db_FILE)
        except Exception:
            self.__cartItemDB = {}
    
    def save_cartItemDB(self):
        if self.__cartItemDB:
            joblib.dump(self.__cartItemDB, CartItemDAO.CART_ITEM_Db_FILE)

    # 항목 추가(이미 있으면 수량 누적)
    def insert_cart_item(self, cart_item):
        id = cart_item.get_member_id()
        book_no = cart_item.get_book_no()
        if id not in self.__cartItemDB:
            self.__cartItemDB[id] = {}
        if book_no in self.__cartItemDB[id]:
            org = self.__cartItemDB[id][book_no]
            org.set_count(org.get_count() + cart_item.get_count())
        else:
            self.__cartItemDB[id][book_no] = cart_item
        self.save_cartItemDB()
    # 회원 장바구니 전체 항목
    def select_all_cart_items(self, id):
        if id in self.__cartItemDB:
            return list(self.__cartItemDB[id].values())
        return []
    # 항목 단건 삭제
    def delete_cart_item(self, id, book_no):
        if id in self.__cartItemDB and book_no in self.__cartItemDB[id]:
            self.__cartItemDB[id].pop(book_no)
            self.save_cartItemDB()
            return True
        return False
    # 회원 장바구니 전체 비우기
    def delete_all_cart_item(self, id):
        if id in self.__cartItemDB:
            self.__cartItemDB[id] = {}
            self.save_cartItemDB()
            return True
        return False

if __name__ == '__main__':
    dao = CartItemDAO()