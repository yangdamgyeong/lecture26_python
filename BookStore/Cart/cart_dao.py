from Cart.cart import Cart
import joblib

class CartDAO:
    CART_DB_FILE = 'cartDB.pkl'
    def __init__(self):
        self.__load_cartDB()

    def __load_cartDB(self):
        try:
            self.__cartDB = joblib.load(CartDAO.CART_DB_FILE)
        except Exception:
            self.__cartDB = {}
    
    def save_cartDB(self):
        if self.__cartDB:
            joblib.dump(self.__cartDB, CartDAO.CART_DB_FILE)
    
    # 장바구니 생성
    def insert_cart(self, cart):
        self.__cartDB[cart.get_member_id()] = cart
        self.save_cartDB()
    # 장바구니 존재 확인
    def is_cart_exist(self, member_id):
        if member_id in self.__cartDB.keys():
            return True
        return False
    # 장바구니 조회
    def select_cart_info(self, member_id):
        if self.is_cart_exist(member_id):
            return self.__cartDB[member_id]
        else:
            return None
    #장바구니 삭제
    def delete_cart(self, member_id):
        if self.is_cart_exist(member_id):
            self.__cartDB.pop(member_id)
            self.save_cartDB()
            return True
        return False

if __name__ == '__main__':
    dao = CartDAO()