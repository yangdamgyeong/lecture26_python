from Member.member_dao import MemberDAO
from Member.member import Member
from Cart.cart import Cart

class MemberService:
    ADMIN_ID = 'admin'
    ADMIN_PASSWORD = '1234'

    def __init__(self, memberDAO, cartDAO):
        self.__dao = memberDAO
        self.__cart_dao = cartDAO
        self.current_user = None

    #아이디가 유효한지
    def is_valid_id(self, id):
        if id.isalpha():
            return True
        return False
    
    #회원가입
    def join_member(self, member):
        #대소문자 구별X
        member.set_id(member.get_id().lower())
        if not self.is_valid_id(member.get_id()):
            return False
        #이미 있는 아이디인지 확인
        if self.__dao.is_member_exist(member.get_id()):
            return False
        self.__dao.insert_member(member)
        #회원가입시 장바구니 생성
        if not self.__cart_dao.is_cart_exist(member.get_id()):
            self.__cart_dao.insert_cart(Cart(member.get_id()))
        return True
    
    #관리자-회원 수동 추가
    def register_member_by_admin(self, member):
        if self.current_user != MemberService.ADMIN_ID:
            return False
        return self.join_member(member)
    
    def login(self, id, password):
        if id == MemberService.ADMIN_ID and password == MemberService.ADMIN_PASSWORD:
            self.current_user = id
            return True
        
        member = self.__dao.select_member_info(id.lower())
        if member:
            if password == member.get_password():
                self.current_user = member.get_id()
                return True
            return False
    
    def logout(self):
        self.current_user = None
        self.__dao.save_memberDB()

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
        if not member:
            return False
        if member.get_password() == org_password:
            member.set_password(new_password)
            return self.__dao.update_member_info(id, member)
        return False
    
    def block_member(self, id):
        if self.current_user != MemberService.ADMIN_ID:
            return False
        if id == MemberService.ADMIN_ID:
            return False
        self.__cart_dao.delete_cart(id)
        return self.__dao.delete_member(id)
    
    def process_member_withdrawal(self, id):
        if self.current_user != id:
            return False
        self.__cart_dao.delete_cart(id)

if __name__ == '__main__':
    from Cart.cart_dao import CartDAO
    ms = MemberService(MemberDAO(), CartDAO())
    print(ms.join_member(Member('yang', '1234', '양담경')))
