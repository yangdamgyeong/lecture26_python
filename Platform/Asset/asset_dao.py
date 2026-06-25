from Asset.asset import Asset
import joblib

class AssetDAO:
    ASSET_DB_FILE = 'assetDB.pkl'

    def __init__(self):
        self.__categories = ['영상', '디자인', '음악']
        self.__asset_seq = 0
        self.__assetDB = {}
        self.__load_assetDB()

    def __load_assetDB(self):
        try:
            self.__assetDB = joblib.load(AssetDAO.ASSET_DB_FILE)
            if self.__assetDB:
                self.__asset_seq = max(self.__assetDB.keys())
        except Exception:
            self.__assetDB = {}

    def save_assetDB(self):
        if self.__assetDB:
            joblib.dump(self.__assetDB, AssetDAO.ASSET_DB_FILE)

    # 자료 신규 등록 (asset_no 자동 생성)
    def insert_asset(self, asset):
        self.__asset_seq += 1
        asset.set_asset_no(self.__asset_seq)
        self.__assetDB[self.__asset_seq] = asset
        self.save_assetDB()
        return self.__asset_seq

    # 자료 존재 확인
    def is_asset_exist(self, asset_no):
        return asset_no in self.__assetDB.keys()

    # 자료 목록
    def select_all_asset(self):
        return list(self.__assetDB.values())

    # 자료 상세
    def select_asset_info(self, asset_no):
        if self.is_asset_exist(asset_no):
            return self.__assetDB[asset_no]
        return None

    # 자료 정보 수정
    def update_asset(self, asset_no, asset):
        if self.is_asset_exist(asset_no):
            asset.set_asset_no(asset_no)
            self.__assetDB[asset_no] = asset
            self.save_assetDB()
            return True
        return False

    # 자료 삭제
    def delete_asset(self, asset_no):
        if self.is_asset_exist(asset_no):
            self.__assetDB.pop(asset_no)
            self.save_assetDB()
            return True
        return False

    def insert_category(self, name):
        if name not in self.__categories:
            self.__categories.append(name)
            return True
        return False # 이미 있는 카테고리

    def get_categories(self):
        """전체 카테고리 목록 조회"""
        return self.__categories

if __name__ == '__main__':
    dao = AssetDAO()
