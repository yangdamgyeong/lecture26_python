from datetime import date

from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Asset.asset import Asset
from Asset.asset_dao import AssetDAO
from Asset.asset_service import AssetService
from Wishlist.wishlist_dao import WishlistDAO
from Wishlist.wishlist_service import WishlistService
from Purchase.purchase_dao import PurchaseDAO
from Purchase.purchase_service import PurchaseService
from Settlement.settlement import Settlement
from Settlement.settlement_dao import SettlementDAO
from Settlement.settlement_service import SettlementService


class OnlineAssetStore:
    guest_menu = ['종료', '자료조회', '로그인', '회원가입']
    member_menu = ['로그아웃', '자료조회', '찜', '구매', '판매', '내정보']
    admin_menu = ['로그아웃', '자료관리', '회원관리', '정산/수익관리']
    wishlist_menu = ['돌아가기', '찜 목록 보기', '찜 담기', '찜 삭제', '다운로드']
    buy_menu = ['돌아가기', '결제', '구매내역', '구매취소']
    sell_menu = ['돌아가기', '자료등록', '내자료관리', '판매내역', '정산요청/조회']
    myinfo_menu = ['돌아가기', '내 정보 조회', '내 정보 수정', '탈퇴']
    admin_asset_menu = ['돌아가기', '자료목록조회', '카테고리관리', '자료강제삭제']
    admin_member_menu = ['돌아가기', '회원목록조회', '회원상세조회', '회원강제탈퇴']
    admin_settle_menu = ['돌아가기', '정산요청목록', '정산승인목록', '정산이력조회']

    def __init__(self):
        # 공용 DAO (의존성 주입)
        member_dao = MemberDAO()
        asset_dao = AssetDAO()
        wishlist_dao = WishlistDAO()
        purchase_dao = PurchaseDAO()
        settlement_dao = SettlementDAO()

        self.msv = MemberService(member_dao)
        self.asv = AssetService(asset_dao)
        self.wsv = WishlistService(wishlist_dao, asset_dao)
        self.psv = PurchaseService(purchase_dao, asset_dao, member_dao)
        self.ssv = SettlementService(settlement_dao, member_dao)

    def main(self):
        self.show_welcome()
        self.run_main_menu()
        self.say_goodbye()

    def show_welcome(self):
        print('========== Yang 영상·디자인 에셋 거래 플랫폼 ==========')

    def say_goodbye(self):
        print(' >> 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        print('-----------------------------------')
        for index in range(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_list[0]}')
        print('-----------------------------------')
        try:
            return int(input(' >> 메뉴 : '))
        except ValueError:
            return -1

    def input_int(self, prompt):
        try:
            return int(input(prompt))
        except ValueError:
            print('숫자만 입력해 주세요.')
            return None

    # ================= 메인 메뉴 =================
    def run_main_menu(self):
        while True:
            user = self.msv.current_user
            if user is None:                       # 비회원
                menu = self.select_menu(self.guest_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_search_assets()
                elif menu == 2:
                    self.menu_login()
                elif menu == 3:
                    self.menu_join()
                else:
                    print('없는 메뉴입니다.')
            elif user == MemberService.ADMIN_ID:   # 관리자
                menu = self.select_menu(self.admin_menu)
                if menu == 0:
                    self.menu_logout()
                elif menu == 1:
                    self.run_admin_asset_menu()
                elif menu == 2:
                    self.run_admin_member_menu()
                elif menu == 3:
                    self.run_admin_settle_menu()
                else:
                    print('없는 메뉴입니다.')
            else:                                  # 회원
                menu = self.select_menu(self.member_menu)
                if menu == 0:
                    self.menu_logout()
                elif menu == 1:
                    self.menu_search_assets()
                elif menu == 2:
                    self.run_wishlist_menu()
                elif menu == 3:
                    self.run_buy_menu()
                elif menu == 4:
                    self.run_sell_menu()
                elif menu == 5:
                    self.run_myinfo_menu()
                else:
                    print('없는 메뉴입니다.')

    # ================= 공통 / 비회원 =================
    def menu_logout(self):
        print('로그아웃 되었습니다.')
        self.msv.logout()

    def menu_join(self):
        print('>>>>>>> 회원가입 <<<<<<<<')
        id = input('> 아이디 : ')
        password = input('> 비밀번호 : ')
        name = input('> 이름 : ')
        email = input('> 이메일 : ')
        member = Member(id, password, name, email)
        member.set_cash(100000)
        if self.msv.join_member(member):
            issued = self.msv.get_member_info(id.lower())
            print(f'회원가입이 완료되었습니다. (회원번호 {issued.get_member_no()})')
        else:
            print('회원가입에 실패했습니다. (중복 아이디이거나 형식 오류)')

    def menu_login(self):
        print('>>>>>>> 로그인 <<<<<<<<')
        id = input('> 아이디 : ')
        password = input('> 비밀번호 : ')
        if self.msv.login(id, password):
            if id == MemberService.ADMIN_ID:
                print('관리자님 환영합니다.')
            else:
                member = self.msv.get_member_info(self.msv.current_user)
                print(f'{member.get_name()}님 환영합니다.')
        else:
            print('로그인에 실패했습니다.')

    def menu_search_assets(self):
        print('>>>>>>> 자료 조회 <<<<<<<<')
        keyword = input('>> 검색어 (제목/카테고리, 전체는 엔터) : ')
        assets = self.asv.search_asset(keyword if keyword else None)
        if not assets:
            print('검색 결과가 없습니다.')
            return
        for asset in assets:
            print(asset)
        asset_no = self.input_int('>> 상세/미리보기할 자료번호 (0 입력 시 취소) : ')
        if not asset_no:
            return
        asset = self.asv.get_asset_info(asset_no)
        if not asset:
            print('없는 자료번호입니다.')
            return
        print('[상세]', asset)
        print(f'[미리보기] {asset.get_preview_url() or "(미리보기 없음)"}')
        # 로그인 회원이면 찜 담기 가능
        if self.msv.current_user and self.msv.current_user != MemberService.ADMIN_ID:
            ans = input('>> 찜에 담으시겠습니까? (y/n) : ')
            if ans.lower() == 'y':
                if self.wsv.add_wishlist(self.msv.current_user, asset_no):
                    print('찜에 담았습니다.')
                else:
                    print('찜 담기에 실패했습니다. (없는 자료이거나 이미 찜함)')

    # ================= 찜 메뉴 =================
    def run_wishlist_menu(self):
        print('>>>>>>> 찜 <<<<<<<<')
        while True:
            menu = self.select_menu(self.wishlist_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_wishlist()
            elif menu == 2:
                self.menu_add_wishlist()
            elif menu == 3:
                self.menu_remove_wishlist()
            elif menu == 4:
                self.menu_download_wishlist()
            else:
                print('없는 메뉴입니다.')

    def menu_list_wishlist(self):
        print('>>>>>>> 찜 목록 (제목만 표시) <<<<<<<<')
        wishes = self.wsv.get_wishlist(self.msv.current_user)
        if not wishes:
            print('찜한 자료가 없습니다.')
            return
        for w in wishes:
            asset = self.wsv.view_asset_detail(w.get_asset_no())
            title = asset.get_title() if asset else '(삭제된 자료)'
            print(f'- {title} (자료번호 {w.get_asset_no()})')

    def menu_add_wishlist(self):
        asset_no = self.input_int('>> 찜할 자료번호 : ')
        if asset_no is None:
            return
        if self.wsv.add_wishlist(self.msv.current_user, asset_no):
            print('찜에 담았습니다.')
        else:
            print('찜 담기에 실패했습니다. (없는 자료이거나 이미 찜함)')

    def menu_remove_wishlist(self):
        asset_no = self.input_int('>> 삭제할 자료번호 : ')
        if asset_no is None:
            return
        if self.wsv.remove_wishlist(self.msv.current_user, asset_no):
            print('찜에서 삭제했습니다.')
        else:
            print('삭제에 실패했습니다.')

    def menu_download_wishlist(self):
        asset_no = self.input_int('>> 다운로드할 자료번호 : ')
        if asset_no is None:
            return
        ok, result = self.psv.download_asset(self.msv.current_user, asset_no)
        print(f'다운로드 시작: {result}' if ok else result)

    # ================= 구매 메뉴 =================
    def run_buy_menu(self):
        print('>>>>>>> 구매 <<<<<<<<')
        while True:
            member = self.msv.get_member_info(self.msv.current_user)
            print(f'(보유 캐시 {member.get_cash():,}원)')
            menu = self.select_menu(self.buy_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_pay()
            elif menu == 2:
                self.menu_purchase_history()
            elif menu == 3:
                self.menu_cancel_purchase()
            else:
                print('없는 메뉴입니다.')

    def menu_pay(self):
        asset_no = self.input_int('>> 구매할 자료번호 : ')
        if asset_no is None:
            return
        ok, msg = self.psv.purchase_asset(self.msv.current_user, asset_no)
        print(msg)

    def menu_purchase_history(self):
        history = self.psv.get_purchase_history(self.msv.current_user)
        if not history:
            print('구매 내역이 없습니다.')
            return
        for p in history:
            print(p)

    def menu_cancel_purchase(self):
        purchase_no = self.input_int('>> 취소할 구매번호 : ')
        if purchase_no is None:
            return
        ok, msg = self.psv.cancel_purchase(purchase_no)
        print(msg)

    # ================= 판매 메뉴 =================
    def run_sell_menu(self):
        print('>>>>>>> 판매 <<<<<<<<')
        while True:
            menu = self.select_menu(self.sell_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_register_asset()
            elif menu == 2:
                self.menu_manage_my_assets()
            elif menu == 3:
                self.menu_sales_history()
            elif menu == 4:
                self.menu_settlement()
            else:
                print('없는 메뉴입니다.')

    def menu_register_asset(self):
        print('>>>>>>> 자료 등록 <<<<<<<<')
        title = input('>> 제목 : ')
        category = input('>> 카테고리 : ')
        price = self.input_int('>> 가격 : ')
        if price is None:
            return
        file_url = input('>> 파일 경로 : ')
        preview_url = input('>> 미리보기 경로 : ')
        no = self.asv.register_asset(
            Asset(0, title, category, price, self.msv.current_user,
                  file_url, preview_url, Asset.ON_SALE))
        print(f'자료를 등록했습니다. (자료번호 {no})')

    def menu_manage_my_assets(self):
        print('>>>>>>> 내 자료 관리 <<<<<<<<')
        my_assets = self.asv.get_my_assets(self.msv.current_user)
        if not my_assets:
            print('등록한 자료가 없습니다.')
            return
        for a in my_assets:
            print(a)
        print('1. 정보수정  2. 판매상태변경  3. 삭제  0. 돌아가기')
        act = self.input_int('>> 작업 : ')
        if not act:
            return
        asset_no = self.input_int('>> 대상 자료번호 : ')
        if asset_no is None:
            return
        asset = self.asv.get_asset_info(asset_no)
        if not asset or asset.get_seller_id() != self.msv.current_user:
            print('내 자료가 아니거나 없는 자료입니다.')
            return
        if act == 1:
            title = input(f'>> 제목 ([{asset.get_title()}]) : ') or asset.get_title()
            category = input(f'>> 카테고리 ([{asset.get_category()}]) : ') or asset.get_category()
            price_in = input(f'>> 가격 ([{asset.get_price()}]) : ')
            price = int(price_in) if price_in.isdigit() else asset.get_price()
            self.asv.update_asset(asset_no,
                Asset(asset_no, title, category, price, asset.get_seller_id(),
                      asset.get_file_url(), asset.get_preview_url(), asset.get_status()))
            print('자료 정보를 수정했습니다.')
        elif act == 2:
            new_status = Asset.STOPPED if asset.get_status() == Asset.ON_SALE else Asset.ON_SALE
            self.asv.change_status(asset_no, new_status)
            print(f'판매 상태를 [{new_status}](으)로 변경했습니다.')
        elif act == 3:
            self.asv.remove_asset(asset_no)
            print('자료를 삭제했습니다.')
        else:
            print('없는 작업입니다.')

    def menu_sales_history(self):
        print('>>>>>>> 판매 내역 <<<<<<<<')
        sales = self.psv.get_sales_history(self.msv.current_user)
        if not sales:
            print('판매 내역이 없습니다.')
            return
        total = 0
        for p in sales:
            print(p)
            total += p.get_price()
        print(f'>> 총 판매액 : {total:,}원')

    def menu_settlement(self):
        print('>>>>>>> 정산 요청 / 조회 <<<<<<<<')
        member = self.msv.get_member_info(self.msv.current_user)
        print(f'(현재 정산 가능 수익 {member.get_revenue():,}원)')
        settlements = self.ssv.view_settlement_status_by_seller(self.msv.current_user)
        if not settlements:
            print('정산 내역이 없습니다.')
        for s in settlements:
            print(s)
        ans = input('>> 정산을 요청하시겠습니까? (y/n) : ')
        if ans.lower() == 'y':
            amount = self.input_int('>> 정산 요청 금액 : ')
            if amount is None:
                return
            ok, msg = self.ssv.request_settlement_info(self.msv.current_user, amount)
            print(msg)

    # ================= 내 정보 메뉴 =================
    def run_myinfo_menu(self):
        print('>>>>>>> 내 정보 <<<<<<<<')
        while True:
            menu = self.select_menu(self.myinfo_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_view_myinfo()
            elif menu == 2:
                self.menu_modify_myinfo()
            elif menu == 3:
                if self.menu_withdrawal():
                    break
            else:
                print('없는 메뉴입니다.')

    def menu_view_myinfo(self):
        print('>>>>>>> 내 정보 조회 <<<<<<<<')
        member = self.msv.get_member_info(self.msv.current_user)
        if member:
            print('[회원 정보]', member)

    def menu_modify_myinfo(self):
        print('>>>>>>> 내 정보 수정 <<<<<<<<')
        member = self.msv.get_member_info(self.msv.current_user)
        if not member:
            return
        print('1. 비밀번호 변경  2. 이메일 변경')
        sel = self.input_int('>> 선택 : ')
        if sel == 1:
            org = input('>> 기존 비밀번호 : ')
            new = input('>> 새 비밀번호 : ')
            if self.msv.update_member_password(self.msv.current_user, org, new):
                print('비밀번호를 변경했습니다.')
            else:
                print('변경에 실패했습니다.')
        elif sel == 2:
            email = input(f'>> 이메일 ([{member.get_email()}]) : ') or member.get_email()
            member.set_email(email)
            if self.msv.modify_member_profile(self.msv.current_user, member):
                print('정보를 변경했습니다.')
        else:
            print('없는 메뉴입니다.')

    def menu_withdrawal(self):
        print('>>>>>>> 탈퇴 <<<<<<<<')
        if input('정말 탈퇴하시겠습니까? (y/n) : ').lower() != 'y':
            print('탈퇴를 취소했습니다.')
            return False
        me = self.msv.current_user
        self.wsv.clear_wishlist(me)
        if self.msv.process_member_withdrawal(me):
            print('탈퇴가 완료되었습니다.')
            self.msv.logout()
            return True
        print('탈퇴에 실패했습니다.')
        return False

    # ================= 관리자 - 자료 관리 =================
    def run_admin_asset_menu(self):
        print('>>>>>>> 자료 관리 <<<<<<<<')
        while True:
            menu = self.select_menu(self.admin_asset_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_admin_list_assets()
            elif menu == 2:
                self.menu_admin_category()
            elif menu == 3:
                self.menu_admin_remove_asset()
            else:
                print('없는 메뉴입니다.')

    def menu_admin_list_assets(self):
        assets = self.asv.search_asset()
        if not assets:
            print('등록된 자료가 없습니다.')
            return
        for a in assets:
            print(a)

    def menu_admin_category(self):
        print('>>>>>>> 카테고리별 자료 수 <<<<<<<<')
        cats = {}
        for a in self.asv.search_asset():
            cats[a.get_category()] = cats.get(a.get_category(), 0) + 1
        if not cats:
            print('등록된 자료가 없습니다.')
        for c, n in cats.items():
            print(f'  {c} : {n}건')

    def menu_admin_remove_asset(self):
        asset_no = self.input_int('>> 강제 삭제할 자료번호 : ')
        if asset_no is None:
            return
        if self.asv.remove_asset(asset_no):
            print('강제 삭제했습니다.')
        else:
            print('없는 자료번호입니다.')

    def menu_admin_category(self):
        print(">> 새로운 카테고리 이름을 입력하세요 : ", end="")
        new_cat = input()
        if self.asv.add_category(new_cat):
            print("카테고리 추가 성공!")
        else:
            print("이미 존재하는 카테고리입니다.")

    # ================= 관리자 - 회원 관리 =================
    def run_admin_member_menu(self):
        print('>>>>>>> 회원 관리 <<<<<<<<')
        while True:
            menu = self.select_menu(self.admin_member_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_admin_list_members()
            elif menu == 2:
                self.menu_admin_member_detail()
            elif menu == 3:
                self.menu_admin_block_member()
            else:
                print('없는 메뉴입니다.')

    def menu_admin_list_members(self):
        members = self.msv.view_all_members()
        if not members:
            print('가입한 회원이 없습니다.')
            return
        for m in members:
            print(m)

    def menu_admin_member_detail(self):
        id = input('>> 조회할 아이디 : ').lower()
        member = self.msv.get_member_info(id)
        print(['상세', member] if member else '없는 회원입니다.')

    def menu_admin_block_member(self):
        id = input('>> 강제 탈퇴할 아이디 : ').lower()
        if self.msv.block_member(id):
            print('강제 탈퇴 처리했습니다.')
        else:
            print('처리에 실패했습니다.')

    # ================= 관리자 - 정산/수익 관리 =================
    def run_admin_settle_menu(self):
        print('>>>>>>> 정산 / 수익 관리 <<<<<<<<')
        while True:
            menu = self.select_menu(self.admin_settle_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_admin_settle_requested()
            elif menu == 2:
                self.menu_admin_settle_approved()
            elif menu == 3:
                self.menu_admin_settle_all()
            else:
                print('없는 메뉴입니다.')

    def menu_admin_settle_requested(self):
        print('>>>>>>> 정산 요청 목록 <<<<<<<<')
        pending = self.ssv.view_settlements_by_status(Settlement.REQUESTED)
        if not pending:
            print('정산 요청이 없습니다.')
            return
        for s in pending:
            print(s)
        if input('>> 처리하시겠습니까? (y/n) : ').lower() != 'y':
            return
        no = self.input_int('>> 정산번호 : ')
        if no is None:
            return
        act = input('>> 승인(a) / 반려(r) : ').lower()
        if act == 'a':
            print(self.ssv.approve_settlement(no)[1])
        elif act == 'r':
            print(self.ssv.reject_settlement(no)[1])
        else:
            print('잘못된 입력입니다.')

    def menu_admin_settle_approved(self):
        print('>>>>>>> 정산 승인 목록 <<<<<<<<')
        approved = self.ssv.view_settlements_by_status(Settlement.APPROVED)
        if not approved:
            print('승인된 정산이 없습니다.')
        for s in approved:
            print(s)

    def menu_admin_settle_all(self):
        print('>>>>>>> 정산 이력 (전체) <<<<<<<<')
        alls = self.ssv.view_all_settlements()
        if not alls:
            print('정산 이력이 없습니다.')
        for s in alls:
            print(s)

    


if __name__ == '__main__':
    app = OnlineAssetStore()
    app.main()
