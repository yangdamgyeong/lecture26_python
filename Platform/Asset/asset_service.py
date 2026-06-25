# service/asset_service.py
from datetime import date  # 요청하신 날짜 라이브러리 추가
from Asset.asset_dao import AssetDAO
from Asset.asset import Asset # 경로가 맞는지 확인하세요

class AssetService:
    """에셋 등록/검색/수정/삭제 비즈니스 로직"""

    def __init__(self,asset_dao):
        self.__assetDAO = AssetDAO()

    def register_asset(self, asset):
        """에셋 등록(업로드) - 등록일자 자동 설정 포함"""
        # asset 객체에 등록일이 없다면 현재 날짜를 설정하는 로직
        if hasattr(asset, 'set_reg_date'):
            asset.set_reg_date(datetime.now().strftime('%Y-%m-%d'))
            
        new_no = self.__assetDAO.insert_asset(asset)
        return new_no

    def search_asset(self, keyword=None):
        """전체 에셋 검색(목록 조회)"""
        assets = self.__assetDAO.select_all_asset()
        # 검색어가 있다면 필터링
        if keyword:
            return [a for a in assets if keyword in a.get_title() or keyword in a.get_category()]
        # 검색어가 없다면 전체 반환
        return assets

    def get_asset_detail(self, asset_no):
        """에셋 상세 조회"""
        return self.__assetDAO.select_asset_info(asset_no)

    def update_asset_info(self, asset_no, asset):
        """에셋 정보 수정"""
        if not self.__assetDAO.is_asset_exist(asset_no):
            return False
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
    
    # Asset/asset_service.py 내부
    def add_category(self, category_name): 
        """새로운 카테고리 추가"""
        return self.__assetDAO.insert_category(category_name)


if __name__ == '__main__':
    svc = AssetService()
    # 예시: Asset 생성자에 데이터 전달
    new_asset = Asset(0, '브이로그 템플릿', '템플릿', 8000, 'user01')
    no = svc.register_asset(new_asset)
    print('등록번호:', no)
    print('검색결과:', [str(a) for a in svc.search_asset()])