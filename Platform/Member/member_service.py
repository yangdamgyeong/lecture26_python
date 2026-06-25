from datetime import date
from Member.member_dao import MemberDAO
from Member.member import Member

class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, memberDAO):
        self.__dao = memberDAO
        self.current_user = None   # None=비회원, 'admin'=관리자, 그 외=회원 id

    # 아이디 유효성 (영문/숫자만 허용)
    def is_valid_id(self, id):
        return id.isalnum()

    # 회원가입
    def join_member(self, member):
        member.set_id(member.get_id().lower())
        if not self.is_valid_id(member.get_id()):
            return False
        if member.get_id() == MemberService.ADMIN_ID:
            return False
        if self.__dao.is_member_exist(member.get_id()):
            return False
        return self.__dao.insert_member(member)

    # 관리자 - 회원 수동 추가
    def register_member_by_admin(self, member):
        if self.current_user != MemberService.ADMIN_ID:
            return False
        return self.join_member(member)

    # 로그인
    def login(self, id, password):
        if id == MemberService.ADMIN_ID and password == MemberService.ADMIN_PASSWORD:
            self.current_user = id
            return True
        member = self.__dao.select_member_info(id.lower())
        if member and member.get_password() == password:
            self.current_user = member.get_id()
            return True
        return False

    def logout(self):
        self.current_user = None

    def get_member_info(self, id):
        return self.__dao.select_member_info(id)

    def view_all_members(self):
        return self.__dao.select_all_members()

    def modify_member_profile(self, id, member):
        if self.current_user != id and self.current_user != MemberService.ADMIN_ID:
            return False
        return self.__dao.update_member_info(id, member)

    def update_member_password(self, id, org_password, new_password):
        if self.current_user != id:
            return False
        member = self.__dao.select_member_info(id)
        if member and member.get_password() == org_password:
            member.set_password(new_password)
            return self.__dao.update_member_info(id, member)
        return False

    # 관리자 - 회원 강제 탈퇴
    def block_member(self, id):
        if self.current_user != MemberService.ADMIN_ID:
            return False
        if id == MemberService.ADMIN_ID:
            return False
        # DAO의 메서드명이 delete_id로 통일되었으므로 수정
        return self.__dao.delete_id(id)

    # 본인 탈퇴
    def process_member_withdrawal(self, id):
        if self.current_user != id:
            return False
        # DAO의 메서드명이 delete_id로 통일되었으므로 수정
        return self.__dao.delete_id(id)

if __name__ == '__main__':
    msv = MemberService(MemberDAO())