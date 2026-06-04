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
        print('-------------------------------------')
        for index in range(1,len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_list[0]}')
        print('-------------------------------------')
        try:
            num = int(input('>>메뉴 : '))
        except ValueError:
            return -1
        else:
            return num

    #시작메뉴
    def run_start_menu(self):
        while True:
            menu = self.select_menu(ConsoleBank.start_menu)
            if menu == 0:
                return
            elif menu == 1: # 로그인
                self.menu_login()
            elif menu == 2: # 회원가입
                self.menu_join()
            else:
                print('없는 메뉴입니다.')
    
    def menu_join(self):
        id = input('> 아이디 입력 : ')
        password = input('> 비밀번호 입력 : ')
        name = input('> 회원명 입력 : ')
        member = Member(id, password, name)
        if self.msv.join(member):
            print('회원가입이 완료되었습니다.')
        else:
            print('회원가입에 실패하였습니다.')

    def menu_login(self):
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

    def menu_logout(self):
        print('안녕히가세요')
        return self.msv.logout()

    #회원 메뉴
    def run_banking_menu(self):
        print('>>>>> 은행 업무 메뉴 <<<<<')
        while True:
            menu = self.select_menu(self.banking_menu)
            if menu == 0:
                self.msv.logout()
                break
            elif menu == 1:
                self.menu_list_my_accounts()
            elif menu == 2:
                self.menu_deposit()
            elif menu == 3:
                self.menu_withdraw()
            elif menu == 4:
                self.menu_create_account()
            elif menu == 5:
                self.menu_delete_account()
            else:
                self.menu_myinfo()

    def menu_list_my_accounts(self):
        self.menu_list_member_accounts()

    def menu_deposit(self):
        print('>>>>> 입금 <<<<<')
        self.menu_list_member_accounts()
        account_no = input('>> 계좌번호 : ')
        try:
            amount = int(input('>> 입금액 : '))
        except ValueError:
            print('숫자만 입력해주세요.')
            return
        if self.asv.deposit(account_no, amount):
            print(f'계좌번호 {account_no}에 {amount}원을 입금했습니다.')
            balance = self.asv.get_account_balance(account_no)
            if balance >= 0:
                print(f'잔액 : {balance}')
        else:
            print('입금을 할 수 없습니다.')

    def menu_withdraw(self):
        print('>>>>> 출금 <<<<<')
        self.menu_list_member_accounts()
        account_no = input('>> 계좌 번호 : ')
        try:
            amount = int(input('>> 출금액 : '))
        except ValueError:
            print('숫자만 입력해주세요.')
            return
        if self.asv.withdraw(account_no, amount):
            print(f'계좌번호 {account_no}에 {amount}원을 출했습니다.')
            balance = self.asv.get_account_balance(account_no)
            if balance >= 0:
                print(f'잔액 : {balance}')
        else:
            print('출금을 할 수 없습니다.')

    def menu_create_account(self):
        print('>>>>> 계좌생성 <<<<<')
        password = input('>> 비밀번호 : ')
        balance = int(input('>> 최초 입금액 : '))
        if self.asv.create_account(Account(0, self.msv.current_user, balance, password)):
            print('계좌를 생성했습니다.')
            self.menu_list_member_accounts()
        else:
            print('계좌 생성에 실패했습니다.')

    def menu_delete_account(self):
        print('>>>>> 계좌해지 <<<<<')
        self.menu_list_member_accounts()

        account_no = input('>>계좌 번호 :')
        password = input('>> 비밀번호 : ')

        try:
            if self.asv.delete_account(self.msv.current_user, account_no, password):
                print(f'계좌번호 {account_no}가 해지되었습니다.')
            else:
                print('계좌 해지에 실패했습니다.')

        except ValueError:
            balance = self.asv.get_account_balance(account_no)
            print(f'잔액 {balance:,}원이 있습니다. 모두 출금 후 계좌를 해지해주세요.')
        except LookupError:
            print('없는 계좌번호입니다.')
        except KeyError:
            print('계좌 해지를 할 수 없습니다.')
        else:
            print('계좌 해지에 실패했습니다.')

    def menu_myinfo(self):
        self.run_my_info_menu()

    #내정보 관리
    def run_my_info_menu(self):
        print('>>>>> 내정보 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.member_myinfo_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_update_password()
            elif menu == 2:
                self.menu_delete_membership()
                break
            else:
                print('없는 메뉴입니다.')

    def menu_view_myinfo(self):
        member = self.msv.view_member_info(self.msv.current_user)
        if member:
            print(member)

    def menu_update_password(self):
        print('>>>>> 비밀번호 수정 <<<<<')
        org_password = input('>> 기존 비밀번호 : ')
        new_password = input('>> 새 비밀번호 : ')
        if self.msv.update_member_password(self.msv.current_user, org_password, new_password):
            print('비밀번호를 변경하였습니다.')
        else:
            print('비밀번호 변경에 실패했습니다.')

    def menu_delete_membership(self):
        check_id = input('>> 본인 확인 ID : ')
        check_password = input('>> 본인 확인 비밀번호 : ')
        if self.msv.remove_member(self.msv.current_user, check_id, check_password):
            print('탈퇴가 되었습니다.')
            self.msv.logout
        else:
            print('탈퇴가 거부되었습니다.')

    #관리자 메뉴
    def run_admin_menu(self):
        print('>>>>> 관리자 업무 메뉴 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.admin_menu)
            if menu == 0:
                self.msv.logout()
                break
            elif menu == 1:
                self.menu_manage_members()
            elif menu == 2:
                self.menu_manage_accounts()
            else:
                print('없는 메뉴입니다.')

    def menu_manage_members(self):
        self.run_admin_member_menu()

    def menu_manage_accounts(self):
        self.run_admin_account_menu()

    #계좌 관리 메뉴
    def run_admin_account_menu(self):
        print('>>>>> 관리자 계좌 관리 메뉴 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.admin_account_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_all_accounts()
            elif menu == 2:
                self.menu_list_member_accounts()
            else:
                print('없는 메뉴입니다.')

    def menu_list_all_accounts(self):
        account_list = self.asv.get_all_accounts()
        if account_list:
            for account in account_list:
                print(account)

    def menu_list_member_accounts(self):
        id = input('> 조회할 회원 아이디 입력 : ')
        account_list = self.asv.get_members_accounts(id)
        if account_list:
            for account in account_list:
                print(account)
        else:
            print('등록된 계좌가 없습니다.')

    #회원 관리 메뉴
    def run_admin_member_menu(self):
        print('>>>>> 관리자 회원 관리 메뉴 <<<<<')
        while True:
            menu = self.select_menu(ConsoleBank.admin_member_menu)
            if menu == 0:
                break
            elif menu == 1:
                self.menu_list_members()
            elif menu == 2:
                self.menu_view_member_info()
            elif menu == 3:
                self.menu_delete_member()
            else:
                print('없는 메뉴 입니다.')

    def menu_list_members(self):
        member_list = self.msv.list_members()
        if member_list:
            for member in member_list:
                print(member)
        else:
            print('가입한 회원이 없습니다.')

    def menu_view_member_info(self):
        id = input('>> 조회할 회원 아이디를 입력하세요 : ')
        member = self.msv.view_member_info(id)
        if member:
            print(member)
        else:
            print('회원이 아닙니다.')

    def menu_delete_member(self): 
        id = input('>> 강퇴할 회원 아이디를 입력하세요 : ')
        if self.msv.remove_member(id):
            print('강퇴 처리되었습니다.')
        else:
            print('강퇴 처리가 어렵습니다.')
        

if __name__ == '__main__':
    app = ConsoleBank()
    app.main()



