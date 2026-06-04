from Member.member import Member
# 회원 데이터 접근 (CRUD) : MemberDAO
class MemberDAO:
    def __init__(self):
        self.__memberDB = {}
#회원가입
    def insert_member(self, member):
        self.__memberDB[member.get_id()] = member
#동일한 아이디 있는지 확인
    def is_exist(self, id):
        if id in self.__memberDB.keys():
            return True
        return False
#회원정보상세
    def get_member_info(self, id):
        if self.is_exist(id):
            return self.__memberDB[id]
        else:
            return None
#회원목록        
    def get_all_members(self):
        if self.__memberDB:
            return list(self.__memberDB.values())
        
    def remove_member(self, id):
        if self.is_exist(id):
            self.__memberDB.pop(id)
            return True
        return False
        
    def update_member(self, id, member):
        if self.is_exist(id):
            self.__memberDB[id] = member
            return True
        return False

# 클래스 동작 테스트(단위테스트, unit test)    
if __name__ == '__main__':
    dao = MemberDAO()
    print(dao.is_exist('yang'))

    member = Member('yang', '1234', '양담경')
    dao.insert_member(member)
    member = Member('dam', '1234', '담경')
    dao.insert_member(member)
    print(dao.get_member_info('yang'))
    print(dao.get_member_info('dam'))

    members = dao.get_all_members()
    for member in members:
        print(member)

    member = dao.get_member_info('yang')
    if member:
        member.set_password('1111')
        dao.update_member_info('yang', member)
    dao.remove_member('yang')
    members = dao.get_all_members()
    for member in members:
        print(member)

