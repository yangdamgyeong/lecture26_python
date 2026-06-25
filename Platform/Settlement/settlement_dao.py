from Settlement.settlement import Settlement
import joblib

class SettlementDAO:
    SETTLEMENT_DB_FILE = 'settlementDB.pkl'

    def __init__(self):
        self.__settlementDB = {}
        self.__load_settlementDB()

    def __load_settlementDB(self):
        try:
            self.__settlementDB = joblib.load(SettlementDAO.SETTLEMENT_DB_FILE)
        except Exception:
            self.__settlementDB = {}

    def save_settlementDB(self):
        joblib.dump(self.__settlementDB, SettlementDAO.SETTLEMENT_DB_FILE)

    # 정산 요청 추가 (정산번호 자동 채번)
    def insert_settlement(self, settlement):
        new_no = max(self.__settlementDB.keys(), default=0) + 1
        settlement.set_settlement_no(new_no)
        self.__settlementDB[new_no] = settlement
        self.save_settlementDB()
        return new_no

    # 특정 판매자의 정산 내역 조회
    def select_settlement_by_seller(self, seller_id):
        return [s for s in self.__settlementDB.values() if s.get_seller_id() == seller_id]

    # 전체 정산 내역 조회 (관리자용)
    def select_all_settlements_admin(self):
        return list(self.__settlementDB.values())

    # 정산 상태 변경 (승인/거절)
    def update_settlement_status(self, settlement_no, status):
        if settlement_no in self.__settlementDB:
            self.__settlementDB[settlement_no].set_settlement_status(status)
            self.save_settlementDB()
            return True
        return False

    # 정산 삭제
    def delete_settlement(self, settlement_no):
        if settlement_no in self.__settlementDB:
            self.__settlementDB.pop(settlement_no)
            self.save_settlementDB()
            return True
        return False

if __name__ == '__main__':
    # 단위 테스트 (필요 시 수정하여 사용)
    dao = SettlementDAO()