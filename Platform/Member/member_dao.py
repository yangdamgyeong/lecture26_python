from Member.member import Member
import joblib

class MemberDAO:
    MEMBER_DB_FILE = 'memberDB.pkl'

    def __init__(self):
        self.__member_seq = 0
        self.__memberDB = {}
        self.__load_memberDB()

    def __load_memberDB(self):
        try:
            self.__memberDB = joblib.load(MemberDAO.MEMBER_DB_FILE)
            if self.__memberDB:
                # 옛 데이터(member_no가 ''나 문자열)일 수 있으니 정수만 골라서 복원
                nos = [m.get_member_no() for m in self.__memberDB.values()
                       if isinstance(m.get_member_no(), int)]
                self.__member_seq = max(nos) if nos else 0
        except Exception:
            self.__memberDB = {}

    def save_memberDB(self):
        joblib.dump(self.__memberDB, MemberDAO.MEMBER_DB_FILE)

    # 회원 신규 등록 (member_no 자동 부여)
    def insert_member(self, member):
        if member.get_id() in self.__memberDB:
            return False
        self.__member_seq += 1
        member.set_member_no(self.__member_seq)
        self.__memberDB[member.get_id()] = member
        self.save_memberDB()
        return True

    # 회원 존재 확인
    def is_member_exist(self, id):
        return id in self.__memberDB

    # 전체 회원 목록
    def select_all_members(self):
        return list(self.__memberDB.values())

    # 특정 회원 정보 조회
    def select_member_info(self, id):
        return self.__memberDB.get(id)

    # 회원 정보 수정
    def update_member_info(self, id, member):
        if self.is_member_exist(id):
            self.__memberDB[id] = member
            self.save_memberDB()
            return True
        return False

    # 회원 삭제
    def delete_id(self, id):
        if self.is_member_exist(id):
            self.__memberDB.pop(id)
            self.save_memberDB()
            return True
        return False

if __name__ == '__main__':
    # 단위 테스트
    dao = MemberDAO()
    # 테스트 코드 작성...