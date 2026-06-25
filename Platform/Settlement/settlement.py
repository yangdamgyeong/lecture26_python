# model/settlement.py
# 정산(판매 수익 정산) 정보를 담는 모델 클래스


class Settlement:
    """판매자의 정산 요청 1건을 표현하는 모델"""
    REQUESTED = '요청'
    APPROVED = '승인'
    REJECTED = '거절'

    def __init__(self, settlement_no=0, seller_id='', amount=0,
                 settlement_status='요청', request_date='', process_date=''):
        self.__settlement_no = settlement_no          # 정산 고유번호 (PK)
        self.__seller_id = seller_id                  # 정산 요청 판매자 ID
        self.__amount = amount                        # 정산 요청 금액
        self.__settlement_status = settlement_status  # 상태 (요청 / 승인 / 거절)
        self.__request_date = request_date            # 요청 날짜
        self.__process_date = process_date            # 처리(승인/거절) 날짜

    # ---------- getters ----------
    def get_settlement_no(self):
        return self.__settlement_no

    def get_seller_id(self):
        return self.__seller_id

    def get_amount(self):
        return self.__amount

    def get_settlement_status(self):
        return self.__settlement_status

    def get_request_date(self):
        return self.__request_date

    def get_process_date(self):
        return self.__process_date

    # ---------- setters ----------
    def set_settlement_no(self, settlement_no):
        self.__settlement_no = settlement_no

    def set_seller_id(self, seller_id):
        self.__seller_id = seller_id

    def set_amount(self, amount):
        self.__amount = amount

    def set_settlement_status(self, settlement_status):
        self.__settlement_status = settlement_status

    def set_request_date(self, request_date):
        self.__request_date = request_date

    def set_process_date(self, process_date):
        self.__process_date = process_date

    def __str__(self):
        return (f"[정산{self.__settlement_no}] 판매자:{self.__seller_id} | "
                f"{self.__amount}원 | {self.__settlement_status} | "
                f"요청:{self.__request_date} | 처리:{self.__process_date}")


if __name__ == '__main__':
    # 단위 테스트
    s = Settlement(1, 'user01', 30000, '요청', '2026-06-25')
    print(s)
    s.set_settlement_status('승인')
    s.set_process_date('2026-06-26')
    print('처리 후:', s)
