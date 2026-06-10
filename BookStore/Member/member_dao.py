from Member.member import Member
import joblib

class MemberDAO:
    def __init__(self):
        self.__load_memberDB()

    def __load_memberDB(self):
        try:
            self.__memberDB = joblib.load(MemberDAO.MEMBER_DB_FILE)
        except Exception:
            self.__memberDB = {}
    
    def save_memberDB(self):
        if self.__memberDB:
            joblib.dump(self.__memberDB, MemberDAO.MEMBER_DB_FILE)

    #회원가입
    def insert_member(self, member):
        self.__memberDB[member.get_id()] = member
        self.save_memberDB
    #동일한 아이디가 있는지 확인
    def is_member_exist(self, id):
        if id in self.__memberDB.keys():
            return True
        return False
    #회원정보상세
    def select_member_info(self, id):
        if self.is_member_exist(id):
            return self.__memberDB[id]
        else:
            return None
    #회원목록
    def select_all_members(self):
        if self.__memberDB:
            return list(self.__memberDB.values())
        return []
    #회원탈퇴
    def delete_member(self, id):
        if self.is_member_exist(id):
            self.__memberDB.pop(id)
            self.save_memberDB()
            return True
        return False
    #회원정보수정
    def update_member_info(self, id, member):
        if self.is_member_exist(id):
            self.__memberDB[id] = member
            self.save_memberDB()
            return True
        return False
    
if __name__ == '__main__':
    dao = MemberDAO()