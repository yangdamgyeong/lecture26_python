#===================
#데이터 모델 정의 : Member
class Member:
    def __init__(self, id, password, name):
        self.__member_no = 0
        self.__id = id
        self.__password = password
        self.__name = name

    def get_member_no(self):
        return self.__member_no    
    def get_id(self):
        return self.__id
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    def set_password(self, password):
        self.__password = password

    def __str__(self):
        return f'{self._member_no}\t{self.__id}\t{self.__name}\n{self.__password}'
    
#====================
#회원 관리 서비스 로직 (Controller) : MemberService
class MemberService:
    def __init__(self,memberDAO):
        self.__dao = memberDAO

    def join(self, member):
        # 이미 있는 아이디인지 확인
        if self.__dao.is_exist(member.get_id()):
            return False
        self.__dao.insert_member(member)
        return True
    
    def login(self, id, password):
        member = self.__dao.get_member_info(id)
        if member:
            if password == member.get_password():
                return id
        return None
    
    def list_members(self):
        member_list = self.__dao.get_all_members()
        return member_list
    
    def get_member_info(self, id):
        return self.__dao.get_member_info(id)
    
    def remove_member(self, id):
        return self.__dao.remove_member(id)
    
    def update_member(self, member):
        return self.__dao.update_member(member)


#====================
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
            del self.__memberDB[id]
            return True
        else:
            return False
        
    def update_member(self, id, member):
        if self.is_exist(member.get_id):
            self.__memberDB[member.get_id] = member
            return True
        return False