class Member:
    def __init__(self, member_no, user_id, password, name, phone, address):
        self.member_no = member_no
        self.user_id = user_id
        self.password = password
        self.name = name
        self.phone = phone
        self.address = address
    def __str__(self):
        return f'{self.__member_no}\t{self.__user_id}\t{self.__password}\t{self.__name}\t{self.__phone}\t{self.__address}'
    
class MemberService:
    def __init__(self):
        self.__member_list = []

    #회원가입
    def create_member(self, member_no, user_id, password, name, phone, address):
        member = Member(member_no, user_id, password, name, phone, address)
        self.__member_list.append(member)
        return True
    #회원목록
    def list_member(self):
        return self.__member_list
    #회원상세정보
    def find_member(self, name):
        for member in self.__member_list:
            if member.name == name:
                return member
        return None
    #회원정보수정
    def edit_member(self, member_no, password, name, phone, address):
        for member in self.__member_list:
            if member.member_no == member_no:
                member.password = password
                member.name = name
                member.phone = phone
                member.address = address
                return True
        return False
    #회원탈퇴
    def del_member(self, user_id):
        for member in self.__member_list:
            if member.user_id == user_id:
                self.__member_list.remove(member)
                return True
        return False