from Cart.cart_dao import CartDAO
from Cart.cart_item_dao import CartItemDAO
from Cart.cart import Cart
from Cart.cart_item import CartItem

class CartService:
    def __init__(self, cartDAO, cartItemDAO):
        self.__cart_dao = cartDAO
        self.__cart_item_dao = cartItemDAO
    
    def add_cart(self, cart):
        if self.__cart_dao.is_cart_exist(cart.get_member_id()):
            return False
        self.__cart_dao.insert_cart(cart)
        return True
    
    def get_cart_info(self, member_id):
        return self.__cart_dao.select_cart_info(member_id)
    
    def clear_cart(self, member_id):
        return self.__cart_item_dao.delete_all_cart_item(member_id)
    
    def add_cart_item(self, member_id, book_no, count):
        #장바구니 생성
        if not self.__cart_dao.is_cart_exist(member_id):
            self.__cart_dao.insert_cart(Cart(member_id))
        if count <= 0:
            return False
        self.__cart_item_dao.insert_cart_item(CartItem(member_id, book_no, count))
        return True
    
    def get_cart_item(self, member_id):
        return self.__cart_item_dao.select_all_cart_items(member_id)
    
    def update_cart_item_count(self, member_id, book_no, count):
        #수량 변경
        items = self.__cart_item_dao.select_all_cart_items(member_id)
        target = None
        for item in items:
            if item.get_book_no() == book_no:
                target = item
                break
            if target is None:
                return False
            if count <= 0:
                return self.__cart_item_dao.delete_cart_item(member_id, book_no)
            self.__cart_item_dao.delete_cart_item(member_id, book_no)
            self.__cart_item_dao.insert_cart_item(CartItem(member_id, book_no, count))
            return True
    
    def remove_cart_item(self, member_id, book_no):
        return self.__cart_item_dao.delete_cart_item(member_id, book_no)
    
if __name__ == '__main__':
    csv = CartService(CartDAO(), CartItemDAO())
    csv.add_cart_item('yang', 1, 2)