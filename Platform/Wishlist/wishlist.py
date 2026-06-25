# model/wishlist.py
# 찜(위시리스트) 정보를 담는 모델 클래스


class Wishlist:
    """회원이 찜한 에셋 1건을 표현하는 모델"""

    def __init__(self, wish_no=0, member_id='', asset_no=0, added_date=''):
        self.__wish_no = wish_no        # 찜 고유번호 (PK)
        self.__member_id = member_id    # 찜한 회원 ID
        self.__asset_no = asset_no      # 찜한 에셋 번호
        self.__added_date = added_date  # 찜한 날짜

    # ---------- getters ----------
    def get_wish_no(self):
        return self.__wish_no

    def get_member_id(self):
        return self.__member_id

    def get_asset_no(self):
        return self.__asset_no

    def get_added_date(self):
        return self.__added_date

    # ---------- setters ----------
    def set_wish_no(self, wish_no):
        self.__wish_no = wish_no

    def set_member_id(self, member_id):
        self.__member_id = member_id

    def set_asset_no(self, asset_no):
        self.__asset_no = asset_no

    def set_added_date(self, added_date):
        self.__added_date = added_date

    def __str__(self):
        return (f"[찜{self.__wish_no}] 회원:{self.__member_id} | "
                f"에셋:{self.__asset_no} | {self.__added_date}")


if __name__ == '__main__':
    # 단위 테스트
    w = Wishlist(1, 'user01', 3, '2026-06-25')
    print(w)
