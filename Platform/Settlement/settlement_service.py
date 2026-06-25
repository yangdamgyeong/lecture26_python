# service/settlement_service.py
# 정산(판매 수익 정산) 관련 비즈니스 로직을 처리하는 Service

from datetime import date

from Settlement.settlement_dao import SettlementDAO
from Member.member_dao import MemberDAO
from Settlement.settlement import Settlement


class SettlementService:
    """정산 요청/승인/거절 비즈니스 로직"""

    def __init__(self,settlement_dao, member_dao):
        self.__settlementDAO = settlement_dao
        self.__memberDAO = member_dao

    def request_settlement_info(self, seller_id, amount):
        """
        정산 요청 (판매자가 수익 정산을 신청)
        반환: (성공여부, 메시지)
        """
        seller = self.__memberDAO.select_member_info(seller_id)
        if seller is None:
            return False, '회원 정보를 찾을 수 없어.'
        if amount <= 0:
            return False, '정산 금액은 1원 이상이어야 해.'
        if seller.get_revenue() < amount:
            return False, f'정산 가능 수익이 부족해. (보유수익:{seller.get_revenue()}원)'

        settlement = Settlement(0, seller_id, amount, '요청', str(date.today()))
        no = self.__settlementDAO.insert_settlement(settlement)
        return True, f'정산 요청 완료! (정산번호:{no})'

    def update_settlement_status(self, settlement_no, status):
        """정산 상태 변경"""
        return self.__settlementDAO.update_settlement_status(settlement_no, status)

    def view_settlement_status_by_seller(self, seller_id):
        """판매자 본인의 정산 현황 조회"""
        return self.__settlementDAO.select_settlement_by_seller(seller_id)

    def view_all_settlements(self):
        """전체 정산 목록 조회 (관리자)"""
        return self.__settlementDAO.select_all_settlements_admin()

    def view_settlements_by_status(self, status):
        """상태별 정산 목록 조회 (요청/승인/거절)"""
        return [s for s in self.__settlementDAO.select_all_settlements_admin()
                if s.get_settlement_status() == status]

    def approve_settlement(self, settlement_no):
        """
        정산 승인 (관리자) - 승인 시 판매자 수익에서 정산액 차감
        반환: (성공여부, 메시지)
        """
        all_s = self.__settlementDAO.select_all_settlements_admin()
        target = next((s for s in all_s
                       if s.get_settlement_no() == settlement_no), None)
        if target is None:
            return False, '존재하지 않는 정산이야.'
        if target.get_settlement_status() != '요청':
            return False, '이미 처리된 정산이야.'

        seller = self.__memberDAO.select_member_info(target.get_seller_id())
        if seller is not None:
            seller.set_revenue(seller.get_revenue() - target.get_amount())
            self.__memberDAO.update_member_info(seller.get_id(), seller)

        target.set_settlement_status('승인')
        target.set_process_date(str(date.today()))
        # 변경 반영 (상태 + 처리일)
        self.__settlementDAO.update_settlement_status(settlement_no, '승인')
        self._apply_process_date(settlement_no, str(date.today()))
        return True, '정산을 승인했어.'

    def reject_settlement(self, settlement_no):
        """
        정산 거절 (관리자)
        반환: (성공여부, 메시지)
        """
        all_s = self.__settlementDAO.select_all_settlements_admin()
        target = next((s for s in all_s
                       if s.get_settlement_no() == settlement_no), None)
        if target is None:
            return False, '존재하지 않는 정산이야.'
        if target.get_settlement_status() != '요청':
            return False, '이미 처리된 정산이야.'

        self.__settlementDAO.update_settlement_status(settlement_no, '거절')
        self._apply_process_date(settlement_no, str(date.today()))
        return True, '정산을 거절했어.'

    def _apply_process_date(self, settlement_no, process_date):
        """내부용: 처리일자 반영"""
        all_s = self.__settlementDAO.select_all_settlements_admin()
        for s in all_s:
            if s.get_settlement_no() == settlement_no:
                s.set_process_date(process_date)
                break
        # DAO에 전체 다시 저장하기 위해 상태 갱신 메서드 재활용
        for s in all_s:
            self.__settlementDAO.update_settlement_status(
                s.get_settlement_no(), s.get_settlement_status())


if __name__ == '__main__':
    from model.member import Member
    m_dao = MemberDAO()
    m_dao.insert_member(Member('sel', 'pw', '셀러', 'sel@test.com', 0, 50000))
    svc = SettlementService()
    print(svc.request_settlement_info('sel', 30000))
    pending = svc.view_settlements_by_status('요청')
    print('요청목록:', [str(s) for s in pending])
    if pending:
        print(svc.approve_settlement(pending[0].get_settlement_no()))
    print('남은수익:', m_dao.select_member_info('sel').get_revenue())
