# model/asset.py
# 에셋(영상/디자인 자료) 정보를 담는 모델 클래스

class Asset:
    """판매되는 영상·디자인 에셋 1건을 표현하는 모델"""
    ON_SALE = '판매중'
    STOPPED = '판매중지'

    def __init__(self, asset_no, title, category, price, seller_id, file_url, preview_url, status):
        self.__asset_no = asset_no          # 에셋 고유번호 (PK)
        self.__title = title                # 제목
        self.__category = category          # 카테고리 (영상/이미지/템플릿 등)
        self.__price = price                # 가격
        self.__seller_id = seller_id        # 판매자 회원 ID
        self.__file_url = file_url          # 실제 파일 경로(다운로드용)
        self.__preview_url = preview_url    # 미리보기 경로
        self.__status = status              # 상태 (판매중 / 판매중지 / 삭제)

    # ---------- getters ----------
    def get_asset_no(self):
        return self.__asset_no

    def get_title(self):
        return self.__title

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price

    def get_seller_id(self):
        return self.__seller_id

    def get_file_url(self):
        return self.__file_url

    def get_preview_url(self):
        return self.__preview_url

    def get_status(self):
        return self.__status

    # ---------- setters ----------
    def set_asset_no(self, asset_no):
        self.__asset_no = asset_no

    def set_title(self, title):
        self.__title = title

    def set_category(self, category):
        self.__category = category

    def set_price(self, price):
        self.__price = price

    def set_seller_id(self, seller_id):
        self.__seller_id = seller_id

    def set_file_url(self, file_url):
        self.__file_url = file_url

    def set_preview_url(self, preview_url):
        self.__preview_url = preview_url

    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return (f"[{self.__asset_no}] {self.__title} | {self.__category} | "
                f"{self.__price}원 | 판매자:{self.__seller_id} | {self.__status}")


if __name__ == '__main__':
    # 단위 테스트
    a = Asset(1, '시네마틱 인트로 영상', '영상', 15000, 'user01',
              'files/intro.mp4', 'preview/intro.jpg')
    print(a)
    a.set_price(20000)
    print('가격 변경 후:', a.get_price())
