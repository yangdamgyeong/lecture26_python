# model/member.py
# 회원 정보를 담는 모델 클래스


class Member:
    """사이트 회원 1명을 표현하는 모델"""

    def __init__(self, id='', password='', name='', email='', cash=0, revenue=0, member_no=0):
        self.__id = id # 회원 ID (PK)
        self.__password = password # 비밀번호
        self.__name = name # 이름
        self.__email = email # 이메일
        self.__cash = cash # 보유 캐시(구매에 사용)
        self.__revenue = revenue # 누적 판매 수익
        self.__member_no = member_no # 고유번호
        

    # ---------- getters ----------
    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_cash(self):
        return self.__cash

    def get_revenue(self):
        return self.__revenue

    def get_member_no(self):
        return self.__member_no

    # ---------- setters ----------
    def set_id(self, id):
        self.__id = id

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_cash(self, cash):
        self.__cash = cash

    def set_revenue(self, revenue):
        self.__revenue = revenue
    
    def set_member_no(self, member_no):
        self.__member_no = member_no

    def __str__(self):
        return (f"회원번호: {self.__member_no} | ID:{self.__id} | {self.__name} | {self.__email} | "
                f"캐시:{self.__cash}원 | 수익:{self.__revenue}원")


if __name__ == '__main__':
    # 단위 테스트
    m = Member('user01', '1234', '양담경', 'dam@test.com', 50000, 0)
    print(m)
    m.set_cash(m.get_cash() - 15000)
    print('구매 후 캐시:', m.get_cash())
