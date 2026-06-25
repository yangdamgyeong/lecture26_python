# service/asset_service.py
from datetime import date
from Asset.asset_dao import AssetDAO
from Asset.asset import Asset

class AssetService:
    """에셋 등록/검색/수정/삭제 비즈니스 로직"""

    def __init__(self, asset_dao):
        # 주입받은 DAO를 그대로 사용 (DI) - 새로 생성하면 데이터가 따로 논다
        self.__assetDAO = asset_dao

    def register_asset(self, asset):
        """에셋 등록(업로드) - 등록된 asset_no 반환"""
        new_no = self.__assetDAO.insert_asset(asset)
        return new_no

    def search_asset(self, keyword=None):
        """전체 에셋 검색(목록 조회). 키워드가 있으면 제목/카테고리로 필터링"""
        assets = self.__assetDAO.select_all_asset()
        if keyword:
            kw = keyword.lower()
            return [a for a in assets
                    if kw in a.get_title().lower() or kw in a.get_category().lower()]
        return assets

    def get_asset_info(self, asset_no):
        """에셋 상세 조회 (Platform이 호출하는 이름으로 통일)"""
        return self.__assetDAO.select_asset_info(asset_no)

    # 이전 이름과의 호환을 위한 별칭
    def get_asset_detail(self, asset_no):
        return self.get_asset_info(asset_no)

    def update_asset(self, asset_no, asset):
        """에셋 정보 수정 (Platform이 호출하는 이름)"""
        if not self.__assetDAO.is_asset_exist(asset_no):
            return False
        return self.__assetDAO.update_asset(asset_no, asset)

    # 이전 이름과의 호환을 위한 별칭
    def update_asset_info(self, asset_no, asset):
        return self.update_asset(asset_no, asset)

    def change_status(self, asset_no, status):
        """판매 상태 변경 (판매중 <-> 판매중지)"""
        asset = self.__assetDAO.select_asset_info(asset_no)
        if not asset:
            return False
        asset.set_status(status)
        return self.__assetDAO.update_asset(asset_no, asset)

    def remove_asset(self, asset_no):
        """에셋 삭제"""
        if not self.__assetDAO.is_asset_exist(asset_no):
            return False
        return self.__assetDAO.delete_asset(asset_no)

    def get_my_assets(self, seller_id):
        """내가 등록한 에셋 목록 조회"""
        return [a for a in self.__assetDAO.select_all_asset()
                if a.get_seller_id() == seller_id]

    def add_category(self, category_name):
        """새로운 카테고리 추가"""
        return self.__assetDAO.insert_category(category_name)

    def get_categories(self):
        """전체 카테고리 목록"""
        return self.__assetDAO.get_categories()


if __name__ == '__main__':
    svc = AssetService(AssetDAO())
    no = svc.register_asset(Asset(0, '브이로그 템플릿', '템플릿', 8000, 'user01'))
    print('등록번호:', no)
    print('검색결과:', [str(a) for a in svc.search_asset()])
