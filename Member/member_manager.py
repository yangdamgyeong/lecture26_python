class Member:
    def __init__(self, member_no, user_id, password, phone, address):
        self.member_no = member_no
        self.user_id = user_id
        self.password = password
        self.phone = phone
        self.address = address
    def __str__(self):
        return f'{self.__account_no}\t{self.__user_id}\t{self.__password}\t{self.__phone}\t{self.__address}'
    
class MemberService:
    def __init__(self):
        self.__member_list = []
    def create_member(self, member_no, user_id, password, phone, address):
        member = Member(member_no, user_id, password, phone, address)
        self.__member_list.append(member)
        return True
    
    def list_member(self):
        return self.__member_list
    
    def find_member(self, member_no):
        for member in self.__member_list:
            if member.member_no == member_no:
                return member
        return None
    
    def edit_member(self, member_no, user_id, password, phone, address):
        for member in self.__member_list:
            if member.member_no == member_no:
                member.password = password
                member.phone = phone
                member.address = address
                return True
        return False


def select_menu():
    menu = int(input('>> 메뉴를 고르시오 : '))
    return menu


print('=============================================================================')
print(' 1. 회원 가입 | 2. 회원 목록 | 3. 회원상세정보 | 4. 회원정보수정 | 5. 회원 탈퇴 ')
print('=============================================================================')

mservice = MemberService()
print()

while True:
    menu = select_menu()
    if menu == 5:
        print('회원이 탈퇴되었습니다.')
        break
    elif menu == 1:
        member_no = input("> 이름: ")
        user_id = input("> 아이디: ")
        password = input("> 비밀번호: ")
        phone = input("> 전화번호: ")
        address = input("> 주소: ")

        if mservice.create_member(member_no, user_id, password, phone, address):
            print('회원 가입이 되었습니다.')

    elif menu == 2:
        member_list = mservice.list_member()
        print('------------')
        print(' 회원 목록 ')
        for member in member_list:
            print(member)
        print('------------')

    elif menu == 3:
        search_name = input("> 조회할 이름: ")
        print('-------------')
        print(' 회원상세정보 ')
        print('-------------')
        member = mservice.find_member(search_name)

        if member:
            print(member)
        else:
            print('회원이 아닙니다.')
    elif menu == 4:
        print('-------------')
        print(' 회원정보수정 ')
        print('-------------')
        target_name = input("> 수정할 회원 이름: ")
        member = mservice.find_member(target_name)

        if member:
            while True:
                print(f'[{target_name}]님의 정보를 수정하겠습니다.')
                print(" 1. 비밀번호 | 2. 전화번호 | 3. 주소 | 4. 수정종료 ")
                edit = input("> 수정할 항목 번호: ")

                if edit == '1':
                    member.password = input(">> 새 비밀번호: ")
                    print("비밀번호가 변경되었습니다.")
                elif edit == '2':
                    member.phone = input(">> 새 전화번호: ")
                    print("전화번호가 변경되었습니다.")
                elif edit == '3':
                    member.address = input(">> 새 주소: ")
                    print("주소가 변경되었습니다.")
                elif edit == '4':
                    print("수정을 마칩니다.")
                    break
                else:
                    print("잘못된 선택입니다.")
        else:
            print("수정할 회원을 찾지 못했습니다.")