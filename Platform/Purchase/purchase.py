# model/purchase.py
# 구매 정보를 담는 모델 클래스


class Purchase:
    """에셋 구매 1건을 표현하는 모델"""

    def __init__(self, purchase_no=0, member_id='', asset_no=0, price=0,
                 purchase_date='', status='구매완료'):
        self.__purchase_no = purchase_no    # 구매 고유번호 (PK)
        self.__member_id = member_id        # 구매자 회원 ID
        self.__asset_no = asset_no          # 구매한 에셋 번호
        self.__price = price                # 구매 당시 가격
        self.__purchase_date = purchase_date  # 구매 날짜
        self.__status = status              # 상태 (구매완료 / 구매취소)

    # ---------- getters ----------
    def get_purchase_no(self):
        return self.__purchase_no

    def get_member_id(self):
        return self.__member_id

    def get_asset_no(self):
        return self.__asset_no

    def get_price(self):
        return self.__price

    def get_purchase_date(self):
        return self.__purchase_date

    def get_status(self):
        return self.__status

    # ---------- setters ----------
    def set_purchase_no(self, purchase_no):
        self.__purchase_no = purchase_no

    def set_member_id(self, member_id):
        self.__member_id = member_id

    def set_asset_no(self, asset_no):
        self.__asset_no = asset_no

    def set_price(self, price):
        self.__price = price

    def set_purchase_date(self, purchase_date):
        self.__purchase_date = purchase_date

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return (f"[구매{self.__purchase_no}] 회원:{self.__member_id} | "
                f"에셋:{self.__asset_no} | {self.__price}원 | "
                f"{self.__purchase_date} | {self.__status}")


if __name__ == '__main__':
    # 단위 테스트
    p = Purchase(1, 'user01', 3, 15000, '2026-06-25')
    print(p)
    p.set_status('구매취소')
    print('취소 후:', p.get_status())
