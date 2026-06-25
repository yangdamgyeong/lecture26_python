# service/wishlist_service.py
# 찜(위시리스트) 관련 비즈니스 로직을 처리하는 Service

from datetime import date

from Wishlist.wishlist_dao import WishlistDAO
from Asset.asset_dao import AssetDAO
from Wishlist.wishlist import Wishlist


class WishlistService:
    """찜 추가/조회/삭제 비즈니스 로직"""

    def __init__(self, wishlist_dao, asset_dao):
        self.__wishlistDAO = wishlist_dao
        self.__assetDAO = asset_dao

    def add_wishlist(self, member_id, asset_no):
        """찜 추가"""
        if not self.__assetDAO.is_asset_exist(asset_no):
            return False   # 존재하지 않는 에셋
        if self.__wishlistDAO.is_wishlist_exist(member_id, asset_no):
            return False   # 이미 찜한 에셋
        wish = Wishlist(0, member_id, asset_no, str(date.today()))
        self.__wishlistDAO.insert_wishlist(wish)
        return True

    def get_wishlist(self, member_id):
        """내 찜 목록 조회"""
        return self.__wishlistDAO.select_wishlist_by_member(member_id)

    def remove_wishlist(self, member_id, asset_no):
        """찜 삭제"""
        return self.__wishlistDAO.delete_wishlist(member_id, asset_no)

    def clear_wishlist(self, member_id):
        """찜 전체 비우기"""
        return self.__wishlistDAO.delete_all_wishlist(member_id)

    def view_asset_detail(self, asset_no):
        """찜한 에셋 상세 조회"""
        return self.__assetDAO.select_asset_info(asset_no)


if __name__ == '__main__':
    from model.asset import Asset
    a_dao = AssetDAO()
    no = a_dao.insert_asset(Asset(0, '찜테스트에셋', '영상', 5000, 'seller1'))
    svc = WishlistService()
    print('찜 추가:', svc.add_wishlist('user01', no))
    print('중복 추가:', svc.add_wishlist('user01', no))
    print('내 찜:', [str(w) for w in svc.get_wishlist('user01')])
    svc.remove_wishlist('user01', no)
    print('삭제후 내 찜:', [str(w) for w in svc.get_wishlist('user01')])
