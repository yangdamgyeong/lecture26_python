from Purchase.purchase import Purchase
import joblib

class PurchaseDAO:
    PURCHASE_DB_FILE = 'purchaseDB.pkl'

    def __init__(self):
        self.__purchaseDB = {}
        self.__load_purchaseDB()

    def __load_purchaseDB(self):
        try:
            self.__purchaseDB = joblib.load(PurchaseDAO.PURCHASE_DB_FILE)
        except Exception:
            self.__purchaseDB = {}

    def save_purchaseDB(self):
        joblib.dump(self.__purchaseDB, PurchaseDAO.PURCHASE_DB_FILE)

    # 구매 추가 (구매번호 자동 채번)
    def insert_purchase(self, purchase):
        new_no = max(self.__purchaseDB.keys(), default=0) + 1
        purchase.set_purchase_no(new_no)
        self.__purchaseDB[new_no] = purchase
        self.save_purchaseDB()
        return new_no

    # 특정 회원의 전체 구매 내역 조회
    def select_all_purchases(self, member_id):
        return [p for p in self.__purchaseDB.values() if p.get_member_id() == member_id]

    # 특정 에셋의 구매 내역 조회
    def select_purchases_by_asset(self, asset_no):
        return [p for p in self.__purchaseDB.values() if p.get_asset_no() == asset_no]

    # 특정 구매 1건 조회
    def select_purchase_info(self, purchase_no):
        return self.__purchaseDB.get(purchase_no)

    # 구매 정보 수정
    def update_purchase(self, purchase):
        p_no = purchase.get_purchase_no()
        if p_no in self.__purchaseDB:
            self.__purchaseDB[p_no] = purchase
            self.save_purchaseDB()
            return True
        return False

    # 구매 존재 여부 확인
    def is_purchase_exist(self, purchase_no):
        return purchase_no in self.__purchaseDB

if __name__ == '__main__':
    # 단위 테스트
    dao = PurchaseDAO()
    # (테스트 필요 시 여기에 구현)