from Wishlist.wishlist import Wishlist
import joblib

class WishlistDAO:
    WISHLIST_DB_FILE = 'wishlistDB.pkl'

    def __init__(self):
        self.__wishlistDB = {}
        self.__load_wishlistDB()

    def __load_wishlistDB(self):
        try:
            self.__wishlistDB = joblib.load(WishlistDAO.WISHLIST_DB_FILE)
        except Exception:
            self.__wishlistDB = {}

    def save_wishlistDB(self):
        joblib.dump(self.__wishlistDB, WishlistDAO.WISHLIST_DB_FILE)

    # 찜 추가 (wish_no 자동 채번)
    def insert_wishlist(self, wishlist):
        new_no = max(self.__wishlistDB.keys(), default=0) + 1
        wishlist.set_wish_no(new_no)
        self.__wishlistDB[new_no] = wishlist
        self.save_wishlistDB()
        return new_no

    # 특정 회원의 찜 목록 조회
    def select_wishlist_by_member(self, member_id):
        return [w for w in self.__wishlistDB.values() if w.get_member_id() == member_id]

    # 특정 회원의 특정 에셋 찜 삭제
    def delete_wishlist(self, member_id, asset_no):
        target_keys = [k for k, w in self.__wishlistDB.items() 
                       if w.get_member_id() == member_id and w.get_asset_no() == asset_no]
        
        if not target_keys:
            return False
        
        for k in target_keys:
            self.__wishlistDB.pop(k)
        
        self.save_wishlistDB()
        return True

    # 특정 회원의 찜 전체 삭제
    def delete_all_wishlist(self, member_id):
        target_keys = [k for k, w in self.__wishlistDB.items() if w.get_member_id() == member_id]
        if not target_keys:
            return False
            
        for k in target_keys:
            self.__wishlistDB.pop(k)
        
        self.save_wishlistDB()
        return True

    # 이미 찜한 에셋인지 확인
    def is_wishlist_exist(self, member_id, asset_no):
        return any(w.get_member_id() == member_id and w.get_asset_no() == asset_no 
                   for w in self.__wishlistDB.values())

if __name__ == '__main__':
    # 단위 테스트
    dao = WishlistDAO()