from Member.member_dao import MemberDAO
from Member.member import Member
#====================
#회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self,memberDAO):
        self.__dao = memberDAO
        self.current_user = None
        self.join(Member(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD, '관리자'))

    def join(self, member):
        # 대소문자 구별하지 않음
        member.set_id(member.get_id().lower())
        if not self.is_valid_id(member.get_id()):
            return False
        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False
        
        self.__dao.insert_member(member)
        return True
    

    def is_valid_id(self,id):
        # 아이디가 유효한지 확인
        if id.isalpha():
            return True
        return False
    
    def login(self, id, password):
        member = self.__dao.get_member_info(id)
        if member:
            if password == member.get_password():
                self.current_user = id
                return True
        return False
    
    def logout(self):
        self.current_user = None

    def list_members(self):
        member_list = self.__dao.get_all_members()
        return member_list
    
    def view_member_info(self, id):
        return self.__dao.get_member_info(id)
    
    def get_member_info(self, id):
        return self.__dao.get_member_info(id)
    
    def remove_member(self, id, check_id, check_password):
        if self.current_user == MemberService.ADMIN_ID:
            return self.__dao.remove_member(id)
        elif self.current_user == id:
            if check_id is None or check_password is None:
                return False
            member = self.__dao.get_member_info(id)
            if not member:
                return False
            if member.get_id() == check_id and member.get_password() == check_password:
                return self.__dao.remove_member(id)
        return False
    
    def update_member_info(self, id, member):
        #return self.__dao.update_member_info(id, member)
        result = self.__dao.update_member_info(id, member)

    def update_member_password(self, id, org_password, new_password):
        if self.current_user != id:
            return False
        member = self.__dao.get_member_info(id)
        if not member:
            return False
        if member.get_password() == org_password:
            member.set_password(new_password)
            return True
        return False
    
if __name__ == '__main__':
    ms = MemberService(MemberDAO())
    ms.join(Member('yang', '1234', '양담경'))
    ms.join(Member('dam', '1234', '담경'))
    members = ms.list_members()
    for member in members:
        print(member)
    ms.login('dam', '1234')
    print(ms.current_user)
    ms.logout()
    print(ms.current_user)
    print(ms.view_member_info('dam'))
    ms.login(MemberService.ADMIN_ID, MemberService.ADMIN_PASSWORD)
    print(ms.update_member_password('yang', '1234', '4321'))
    print(ms.view_member_info('yang'))
    print(ms.remove_member('yang'))
    print(ms.view_member_info('yang'))