from member import MemberService

ms = MemberService

def select_menu():
    while True:
        try:
             menu = int(input('>> 메뉴를 고르시오 : '))
             return menu
        except ValueError:
            print('숫자로 입력해주세요.')
print('=====================================================================================')
print(' 1. 회원 가입 | 2. 회원 목록 | 3. 회원상세정보 | 4. 회원정보수정 | 5. 회원 탈퇴 | 0. 종료')
print('=====================================================================================')


mservice = MemberService()
print()

while True:
    menu = select_menu()
    if menu == 0:
        print('회원이 탈퇴되었습니다.')
        break
    elif menu == 1:
        try:
            member_no = input("> 회원번호: ")
            for m in mservice.list_member():
                if m.member_no == member_no:
                    raise Exception('이미 존재하는 회원번호입니다. 다른 번호를 입력하세요.')
            user_id = input("> 아이디: ")
            for m in mservice.list_member():
                if m.user_id == user_id:
                    raise Exception('이미 존재하는 아이디입니다. 다른 아이디를 입력하세요.')
            password = input("> 비밀번호: ")
            name = input("> 이름 :")
            if not name.replace(" ", " ").isalpha():
                raise ValueError('이름에 숫자를 포함할 수 없습니다.')
            phone = input("> 전화번호: ")
            address = input("> 주소: ")

            if mservice.create_member(member_no, user_id, password, name, phone, address):
                print('회원 가입이 되었습니다.')
        except ValueError as e :
            print('이름은 글자만 가능합니다.')
        except Exception as e:
            print(f'다시 시도해주세요. : {e} ({type(e)})')
      

    elif menu == 2:
        try:
            member_list = mservice.list_member()
            print('------------')
            print(' 회원 목록 ')
            if not len(member_list) == 0:
                raise Exception('가입한 회원이 없습니다.')
            for member in member_list:
                print(member)
        except Exception as e:
            print(e)
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
        try: 
            print('-------------')
            print(' 회원정보수정 ')
            print('-------------')
            target_name = input("> 수정할 회원 이름: ")
            member = mservice.find_member(target_name)
            if not member:
                raise Exception('이름이 존재하지 않습니다.')
            print(f'{target_name}님의 정보를 수정합니다.')
        except Exception as e:
            print(e)

        if member:
            while True:
                print(f'[{target_name}]님의 정보를 수정하겠습니다.')
                print(" 1. 비밀번호 | 2. 전화번호 | 3. 주소 | 4. 수정종료 ")
                edit = input("> 수정할 항목 번호: ")
                try:
                    if edit == '1':
                        member.password = input(">> 새 비밀번호: ")
                        for m in mservice.list_member():
                            if m.member_password == password:
                                raise Exception ('비밀번호가 맞지 않습니다.')
                        print("비밀번호가 변경되었습니다.")
                    elif edit == '2':
                        for m in mservice.list_member():
                            if m.phone == phone:
                                raise Exception ('올바른 전화번호를 적어주세요.')
                        member.phone = input(">> 새 전화번호: ")
                        print("전화번호가 변경되었습니다.")
                    elif edit == '3':
                        member.address = input(">> 새 주소: ")
                        for m in mservice.list_member():
                            if m.address == address:
                                raise Exception ('올바른 주소를 적어주세요.')
                        print("주소가 변경되었습니다.")
                    elif edit == '4':
                        print("수정을 마칩니다.")
                        break
                    else:
                        print("잘못된 선택입니다.")
                except Exception as e:
                    print(f'다시 시도해주세요 : {e} ({type(e)})')
    elif menu == 5:
        print('-------------')
        print(' 회원탈퇴')
        print('-------------')
        try:
            user_id = input('탈퇴할 아이디: ')
            if not user_id.strip():
                raise ValueError('아이디를 빈칸으로 둘 수 없습니다.')
            if mservice.del_member(user_id):
                print('회원 탈퇴가 완료되었습니다.')
            else:
                print('탈퇴에 실패했습니다.')
        except Exception as e:
            print('아이디를 작성해주세요.')

            
    else:
        print("회원을 찾지 못했습니다.")