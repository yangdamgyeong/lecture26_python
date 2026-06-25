from datetime import date

from Purchase.purchase_dao import PurchaseDAO
from Purchase.purchase import Purchase
from Asset.asset_dao import AssetDAO
from Member.member_dao import MemberDAO

class PurchaseService:
    def __init__(self, purchaseDAO, assetDAO, memberDAO):
        self.__dao = purchaseDAO
        self.__asset_dao = assetDAO
        self.__member_dao = memberDAO

    # 구매(결제): 무결성 검증 + 캐시 차감 + 판매자 수익 적립
    def purchase_asset(self, member_id, asset_no):
        asset = self.__asset_dao.select_asset_info(asset_no)
        if not asset:
            return False, '존재하지 않는 자료입니다.'
        # 본인 자료 구매 불가
        if asset.get_seller_id() == member_id:
            return False, '본인이 등록한 자료는 구매할 수 없습니다.'
        # 중복 구매 불가
        for p in self.__dao.select_all_purchases(member_id):
            if p.get_asset_no() == asset_no and p.get_status() == Purchase.DONE:
                return False, '이미 구매한 자료입니다.'
        buyer = self.__member_dao.select_member_info(member_id)
        if buyer is None:
            return False, '회원 정보를 찾을 수 없습니다.'
        if buyer.get_cash() < asset.get_price():
            return False, f'캐시가 부족합니다. (보유 {buyer.get_cash():,}원)'

        # 구매자 캐시 차감
        buyer.set_cash(buyer.get_cash() - asset.get_price())
        self.__member_dao.update_member_info(member_id, buyer)
        # 판매자 수익 적립
        seller = self.__member_dao.select_member_info(asset.get_seller_id())
        if seller:
            seller.set_revenue(seller.get_revenue() + asset.get_price())
            self.__member_dao.update_member_info(seller.get_id(), seller)
        # 구매 기록
        no = self.__dao.insert_purchase(
            Purchase(0, member_id, asset_no, asset.get_price(), str(date.today())))
        return True, f'구매가 완료되었습니다. (구매번호 {no})'

    def get_purchase_history(self, member_id):
        return self.__dao.select_all_purchases(member_id)

    def get_purchase_detail(self, purchase_no):
        return self.__dao.select_purchase_info(purchase_no)

    # 구매 취소: 캐시 환불 + 판매자 수익 원복
    def cancel_purchase(self, purchase_no):
        purchase = self.__dao.select_purchase_info(purchase_no)
        if not purchase:
            return False, '존재하지 않는 구매내역입니다.'
        if purchase.get_status() == Purchase.CANCELED:
            return False, '이미 취소된 구매입니다.'

        buyer = self.__member_dao.select_member_info(purchase.get_member_id())
        if buyer:
            buyer.set_cash(buyer.get_cash() + purchase.get_price())
            self.__member_dao.update_member_info(buyer.get_id(), buyer)
        asset = self.__asset_dao.select_asset_info(purchase.get_asset_no())
        if asset:
            seller = self.__member_dao.select_member_info(asset.get_seller_id())
            if seller:
                seller.set_revenue(seller.get_revenue() - purchase.get_price())
                self.__member_dao.update_member_info(seller.get_id(), seller)
        purchase.set_status(Purchase.CANCELED)
        self.__dao.update_purchase(purchase)
        return True, '구매가 취소되고 캐시가 환불되었습니다.'

    # 다운로드 (구매한 회원만)
    def download_asset(self, member_id, asset_no):
        bought = any(p.get_asset_no() == asset_no and p.get_status() == Purchase.DONE
                     for p in self.__dao.select_all_purchases(member_id))
        if not bought:
            return False, '구매하지 않은 자료는 다운로드할 수 없습니다.'
        asset = self.__asset_dao.select_asset_info(asset_no)
        if not asset:
            return False, '자료를 찾을 수 없습니다.'
        return True, asset.get_file_url()

    # 판매 내역 (내 자료가 팔린 구매)
    def get_sales_history(self, seller_id):
        my_asset_nos = [a.get_asset_no()
                        for a in self.__asset_dao.select_all_asset()
                        if a.get_seller_id() == seller_id]
        sales = []
        for asset_no in my_asset_nos:
            sales.extend(self.__dao.select_purchases_by_asset(asset_no))
        return [p for p in sales if p.get_status() == Purchase.DONE]

if __name__ == '__main__':
    psv = PurchaseService(PurchaseDAO(), AssetDAO(), MemberDAO())
