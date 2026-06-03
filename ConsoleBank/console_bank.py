from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Account.account import Account
from Account.account_dao import AccountDAO
from Account.account_service import AccountService

class ConsoleBank:
    start_menu = ['종료', '로그인', '회원가입']
    banking_menu = ['로그아웃', '계좌목록', '입금', '출금', '계좌생성', '계좌해지', '내정보']
    member_myinfo_menu = ['돌아가기', '비밀번호수정', '회원탈퇴']
    admin_menu = ['로그아웃', '회원관리', '계좌관리']
    admin_account_menu = ['돌아가기', '전체계좌목록', '회원별계좌목록']
    admin_member_menu = ['돌아가기', '회원목록', '회원정보조회', '회원강퇴']

    def __init__(self):
        self.msv = MemberService(MemberDAO())
        self.asv = AccountService(AccountDAO())

    def main(self):
        self.show_welcome()
        self.run_start_menu()
        self.say_goodbye()

    def show_welcome(self):
        print('========Yang Console Bank ==========')

    def say_goodbye(self):
        print('>> Yang Console Bank를 이용해 주셔서 감사합니다.')

    def select_menu(self, menu_list):
        return 0

    #시작메뉴
    def run_start_menu():
        while True:
            menu = self.select_menu(ConsoleBank.START_MENU)
            if menu == 0:
                return
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            else:
                print('없는 메뉴입니다.')
    
    def menu_join():
        id = input('> 아이디 입력 : ')
        password = input('> 비밀번호 입력 : ')
        name = input('> 회원명 입력 : ')
        member = Member(id, password, name)
        if self.msv.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다.')

    def menu_login():
        id = input('> 아이디 입력 : ')
        password = input('> 비밀번호 입력 : ')
        if self.msv.login(id, password):
            print(f'{self.msv.view_member_info(id).get_name()}님 환영합니다 !')
            if self.msv.current_user == MemberService.ADMIN_ID:
                self.run_admin_menu()   
            else:
                self.msv.current_user = id
                self.run_banking_menu() 
        else:
            print('로그인에 실패하였습니다.')

    def menu_logout():
        return self.msv.logout()

    #회원 메뉴
    def run_banking_menu():
        pass

    def menu_list_my_accounts():
        pass

    def menu_deposite():
        pass

    def menu_withdraw():
        pass

    def menu_create_account():
        pass

    def menu_delete_account():
        pass

    def menu_myinfo():
        pass

    #내정보 관리
    def run_my_info_menu():
        pass

    def menu_view_myinfo():
        pass

    def menu_update_password():
        pass

    def menu_delete_membership():
        pass

    #관리자 메뉴
    def run_admin_menu():
        pass

    def menu_manage_members():
        pass

    def menu_manage_accounts():
        pass

    #계좌 관리 메뉴
    def run_admin_account_menu():
        pass

    def menu_list_all_accounts():
        pass

    def menu_list_member_accounts():
        pass

    #회원 관리 메뉴
    def run_admin_member_menu():
        pass

    def menu_list_members():
        pass

    def menu_view_member_info():
        pass

    def menu_delete_member():
        pass

if __name__ == '__main__':
    app = ConsoleBank()
    app.main()




