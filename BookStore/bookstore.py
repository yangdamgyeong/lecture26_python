from Member.member import Member
from Member.member_dao import MemberDAO
from Member.member_service import MemberService
from Book.book import Book
from Book.book_dao import BookDAO
from Book.book_service import BookService
from Cart.cart_item_dao import CartItemDAO
from Cart.cart_dao import CartDAO
from Cart.cart_service import CartService
from Order.order_item_dao import OrderItemDAO
from Order.order_dao import OrderDAO
from Order.order_service import OrderService
from Delivery.delivery import Delivery
from Delivery.delivery_dao import DeliveryDAO
from Delivery.delivery_service import DeliveryService



class OnlineBookStore:
    start_menu= ['종료','로그인', '회원가입', '도서조회']
    member_menu= ['로그아웃', '장바구니', '주문조회', '배송조회', '내정보']
    myinfo_menu = ['돌아가기', '내 정보 조회', '내 정보 수정', '탈퇴 신청']
    admin_menu = ['로그아웃', '도서관리', '회원관리', '주문관리', '배송관리']
    admin_order_menu = ['돌아가기', '주문목록조회', '주문상세조회', '주문상태관리', '주문취소']
    admin_member_menu = ['돌아가기', '회원수동추가', '회원정보조회', '회원정보수정', '회원탈퇴']
    admin_book_menu = ['돌아가기', '도서신규등록', '도서목록조회', '도서정보수정', '도서삭제']
    admin_delivery_menu = ['돌아가기', '배송목록조회', '배송상세조회', '배송상태수정', '배송 취소']

    def __init__(self):
        #공용 DAO(의존성 주입)
        member_dao = MemberDAO()
        book_dao = BookDAO()
        cart_dao = CartDAO()
        cart_item_dao = CartItemDAO()
        order_dao = OrderDAO()
        order_item_dao = OrderItemDAO()
        delivery_dao = DeliveryDAO()

        self.msv = MemberService(member_dao, cart_dao)
        self.bsv = BookService(book_dao)
        self.csv = CartService(cart_dao, cart_item_dao)
        self.osv = OrderService(order_dao, order_item_dao, cart_dao)
        self.dsv = DeliveryService(delivery_dao)

    def main(self):
        self.show_welcome()
        self.run_main_menu()
        self.say_goodbye()

    def show_welcome(self):
        print('========== Yang BookStore ===========')

    def say_goodbye(self):
        print(' >> Yang BookStore를 이용해 주셔서 감사합니다. ')

    def select_menu(self, menu_list):
        print('-----------------------------------')
        for index in range(1, len(menu_list)):
            print(f'{index}. {menu_list[index]}')
        print(f'0. {menu_list[0]}')
        print('------------------------------------')
        try:
            num = int(input(' >> 메뉴 :'))
        except ValueError:
            return -1
        else:
            return num
        
    def input_int(self, prompt):
        # 숫자 입력 공용 처리 (실패 시 None)
        try:
            return int(input(prompt))
        except ValueError:
            print('숫자만 입력해주세요.')
            return None
        
    #메인메뉴
    def run_main_menu(self):
        while True:
            user = self.msv.current_user
            if user is None: #비회원
                menu = self.select_menu(self.guest_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_login()
                elif menu == 2:
                    self.menu_join()
                elif menu == 3:
                    self.menu_search_books()
                else:
                    print('없는 메뉴입니다.')
            elif user == MemberService.ADMIN_ID: #관리자
                menu = self.select_menu(OnlineBookStore.admin_menu)
                if menu == 0:
                    self.menu_logout()
                elif menu == 1:
                    self.menu_search_books()
                elif menu == 2:
                    self.run_admin_book_menu()
                elif menu == 3:
                    self.run_admin_member_menu()
                elif menu == 4:
                    self.run_admin_order_menu()
                elif menu == 5:
                    self.run_admin_delivery_menu()
                else:
                    print('없는 메뉴입니다.')
            else: #회원
                menu = self.select_menu(OnlineBookStore.member_menu)
                if menu == 0:
                    self.menu_logout()
                elif menu == 1:
                    self.menu_search_books()
                elif menu == 2:
                    self.run_cart_menu()
                elif menu == 3:
                    self.menu_view_my_orders()
                elif menu == 4:
                    self.menu_view_my_deliveries()
                elif menu == 5:
                    self.run_myinfo_menu()
                else:
                    print('없는 메뉴입니다.')
                
    def menu_logout(self):
        print('로그아웃 되었습니다.')
        self.msv.logout()

    def menu_join(self):
        print('>>>>>>> 회원가입 <<<<<<<<')
        id = input('> 아이디 입력 : ')
        password = input('> 비밀번호 입력 : ')
        name = input('> 회원명 입력 : ')
        email = input('> 이메일 입력 : ')
        address = input('> 주소 입력 : ')
        member = Member(id, password, name, email, address)
        if self.msv.join_member(member):
            print('회원 가입이 완료되었습니다.')
        else:
            print('회원 가입에 실패하였습니다.')

        def menu_login(self):
            print('>>>>>>> 로그인 <<<<<<<<')
            id = input('> 아이디 입력 : ')
            password = input('> 비밀번호 입력 : ')
            if self.msv.login(id, password):
                member = self.msv.get_member_info(self.msv.current_user)
                print(f'{member.get_name()}님 환영합니다.')
            else:
                print('로그인에 실패했습니다.')
        
        def menu_search_books(self):
            print('>>>>>>> 도서 검색 <<<<<<<<')
            keyword = input('>> 검색어 : ')
            books = self.bsv.search_book(keyword if keyword else None)
            if not books:
                print('검색 결과가 없습니다.')
                return
            for book in books:
                print(book)
            book_no = self.input_int('>> 상세 조회할 도서번호 : ')
            if not book_no:
                return
            book = self.bsv.get_book_info(book_no)
            if not book:
                print('없는 도서번호입니다.')
                return
            print('[상세]', book)
            #로그인한 회원이면 장바구니 담기 가능
            if self.msv.current_user and self.msv.current_user != MemberService.ADMIN_ID:
                ans = input('>> 장바구니에 담으시겠습니까? (y/n) : ')
                if ans.lower() == 'y':
                    count = self.input_int('>> 수량 : ')
                    if count and count > 0:
                        if self.csv.add_cart_item(self.msv.current_user, book_no, count):
                            print('장바구니에 담았습니다.')
                        else:
                            print('장바구니 담기에 실패했습니다.')

        #회원 메뉴
        def menu_view_my_orders(self):
            print('>>>>>>> 주문 조회 <<<<<<<<')
            orders = self.osv.get_order_info(self.msv.current_user)
            if not orders:
                print('주문 내역이 없습니다.')
                return
            for order in orders:
                print(order)
                for item in self.osv.get_order_item(order.get_order_no()):
                    book = self.bsv.get_book_info(item.get_book_no())
                    title = book.get_title() if book else '(삭제된 도서)'
                    print(f'  - {title} {item.get_count()}권 ({item.get_price():, }원)')
        def menu_view_my_deliveries(self):
            print('>>>>>>> 배송 조회 <<<<<<<<')
            orders = self.osv.get_order_info(self.msv.current_user)
            if not orders:
                print('주문 내역이 없습니다. ')
                return
            found = False
            for order in orders:
                delivery = self.dsv.view_delivery_status_by_order(order.get_order_no())
                if delivery:
                    found = True
                    print(delivery)
            if not found:
                print('배송 정보가 없습니다.')

        # 장바구니 메뉴
        def run_cart_menu(self):
            print('>>>>>>> 장바구니 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.cart_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_place_order()
                elif menu == 2:
                    self.menu_list_cart_items()
                elif menu == 3:
                    self.menu_update_cart_count()
                elif menu == 4:
                    self.menu_remove_cart_items()
                else:
                    print('없는 메뉴입니다.')

        def menu_list_cart_items(self):
            print('>>>>>>> 장바구니 목록<<<<<<<<')
            items = self.csv.get_cart_item(self.msv.current_user)
            if not items:
                print('장바구니가 비어 있습니다.')
                return
            total = 0
            for item in items:
                book = self.bsv.get_book_info(item.get_book_no())
                if book:
                    subtotal = book.get_price() * item.get_count()
                    total += subtotal
                    print(f'[{book.get_book_no()}] {book.get_title()}\t'f'{item.get_count()}권\t{subtotal:,}원')
                else:
                    print(f'[{item.get_book_no()}] (삭제된 도서)\t{item.get_count()}권')
            print(f'>> 합계 : {total:,}원')

        def menu_update_cart_count(self):
            print('>>>>>>> 장바구니 수량 변경 <<<<<<<<')
            self.menu_list_cart_items()
            book_no = self.input_int(' >> 도서번호 : ')
            if book_no is None:
                return
            count = self.input_inf(' >> 변경할 수량 : ')
            if count is None:
                return
            if self.csv.update_cart_item_count(self.msv.current_user, book_no, count):
                print(' 수량을 변경했습니다. ')
            else:
                print(' 수량 변경에 실패했습니다. ')
        
        def menu_remove_cart_items(self):
            print('>>>>>>> 도서 삭제/ 초기화 <<<<<<<<')
            print(' 1. 도서 삭제 2. 장바구니 초기화 ')
            sel = self.input_int('>> 선택 : ')
            if sel == 1:
                book_no = self.input_int('>> 삭제할 도서번호 : ')
                if book_no is None:
                    return
                if self.csv.remove_cart_item(self.msv.current_user, book_no):
                    print('도서를 삭제했습니다. ')
                else:
                    print('식제에 실패했습니다.')
            elif sel == 2:
                self.csv.clear_cart(self.msv.current_user)
                print('장바구니를 초기화했습니다.')
            else:
                print('없는 메뉴입니다.')

        def menu_place_order(self):
            print('>>>>>>> 주문하기 <<<<<<<<')
            items = self.csv.get_cart_item(self.msv.current_user)
            if not items:
                print('장바구니가 비어 있습니다.')
                return
            #재고 검증 및 합계 계산
            total = 0
            for item in items:
                book = self.bsv.get_book_info(item.get_book_no())
                if not book:
                    print(f'도서 번호 {item.get_book_no()}는 판매 중단되어 주문할 수 없습니다.')
                    return
                if book.get_stock() < item.get_count():
                    print(f'[{book.get_title()}] 재고 부족 (재고 {book.get_stock()}권)')
                    return
                total += book.get_price() * item.get_count()

            member = self.msv.get_member_infp(self.msv.current_user)
            default_addr = member.get_address() if member and member.get_address() else ''
            address = input(f' >> 배송ㄷ지 입력 (엔터 시 [{default_addr}]) : ') or default_addr
            if not address:
                print('배송지가 필요합니다.')
                return
            #주문 생성
            order_no = self.osv.add_order(Order(0, self.msv.current_user, total, order_date))
            for item in items:
                book = self.bsv.get_book_info(item.get_book_no())
                self.osv.add_order_item(order_no, item.get_book_no(), item.get_count(), book.get_price())
                self.bsv.reduce_stock(item.get_book_no(), item.get_count())
            #배송 정보 생성
            self.dsv.register_delivery_info(Delivery(0, order_no, address))
            #장바구니 비우기
            self.csv.clear_cart(self.msv.current_user)
            print(f'주문이 완료되었습니다. (주문 번호 {order_no}, 합계 {total: , }원)')

        #내 정보 메뉴
        def run_myinfo_menu(self):
            print('>>>>>>> 내 정보 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.myinfo_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_view_myinfo()
                elif menu == 2:
                    self.menu_modify_myinfo()
                elif menu == 3:
                    if self.menu_withdrawal():
                        break
                else:
                    print(' 없는 메뉴 입니다. ')
        
        def menu_view_myinfo(self):
            print('>>>>>>> 내 정보 조회 <<<<<<<<')
            member = self.msv.get_member_info(self.msv.current_user)
            if member:
                print('[회원 정보]', member)
            #주문 / 배송 요약
            orders = self.osv.get_order_info(self.msv.current_user)
            print(f'[주문] 총 {len(orders)}건')
            for order in orders:
                delivery = self.dsv.view_delivery_status_by_order(order.get_order_no())
                status = delivery.get_delivery_status() if delivery else '-'
                print(f'   {order}\t배송상태 [{status}]')

        def menu_modify_myinfo(self):
            print('>>>>>>> 내 정보 변경 <<<<<<<<')
            member = self.msv.get_member_info(self.msv.current_user)
            if not member:
                print('회원 정보가 없습니다.')
                return
            print('1. 비밀번호 변경 2. 이메일/주소 변경')
            sel = self.input_int('>> 선택 : ')
            if sel == 1:
                org_password = input('>> 기존 비밀번호 :')
                new_password = input('>> 새 비밀번호 : ')
                if self.msv.update_member_password(self.msv.current_user, org_password, new_password):
                    print('비밀번호를 변경했습니다.')
                else:
                    print('비밀번호 변경에 실패했습니다.')
            elif sel == 2:
                email = input(f' >> 이메일 ([{member.get_email()}]) : ') or member.get_email()
                address = input(f' >> 주소 ([{member.get_address()}]) : ') or member.get_address()
                member.set_email(email)
                member.set_address(address)
                if self.msv.modify_member_profile(self.msv.current_user, member):
                    print('정보를 변경했습니다.')
                else:
                    print('변경에 실패했습니다.')
            else:
                print('없는 메뉴입니다.')

        def menu_withdrawal(self):
            print('>>>>>>> 탈퇴 신청 <<<<<<<<')
            check = input('정말 탈퇴하시겠습니까? (y/n) : ')
            if check.lower() != 'y':
                print('탈퇴를 취소했습니다.')
                return False
            if self.msv.process_member_withdrawal(self.msv.current_user):
                print('탈퇴가 완료되었습니다.')
                self.msv.logout()
                return True
            else:
                print('탈퇴에 실패했습니다.')
                return False
        
        # 관리자 기능
        # 도서 관리 메뉴
        def run_admin_book_menu(self):
            print('>>>>>>> 도서 관리 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.admin_book_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_register_book()
                elif menu == 2:
                    self.menu_list_books()
                elif menu == 3:
                    self.menu_update_book()
                elif menu == 4:
                    self.menu_remove_book()
                else:
                    print('없는 메뉴입니다.')

        def menu_register_book(self):
            print('>>>>>>> 도서 신규 등록 <<<<<<<<')
            title = input(' >> 제목 : ')
            author = input(' >> 저자 : ')
            publisher = input(' >> 출판사 : ')
            price = self.input_int(' >> 가격 : ')
            if price is None:
                return
            stock = self.input(int(' >> 재고 : '))
            if stock is None:
                return
            no = self.bsv.register_book(Book(0, title, author, publisher, price, stock))
            print(f' 도서를 등록했습니다. (도서번호 {no})')

        def menu_list_books(self):
            print('>>>>>>> 도서 목록 및 상세 조회 <<<<<<<<')
            books = self.bsv.search_book()
            if not books:
                print('등록된 도서가 없습니다.')
                return
            for book in books:
                print(book)

        def menu_update_book(self):
            print('>>>>>>> 도서 정보 및 재고 수정 <<<<<<<<')
            self.menu_list_books()
            book_no = self.input(int('>> 수정할 도서번호 : '))
            if book_no is None:
                return
            book = self.bsv.get_book_myinfo(book_no)
            if not book:
                print('없는 도서 번호입니다.')
                return
            title = input(f'>> 제목 ([{book.get_title()}]) : ') or book.get_title()
            author = input(f'>> 저자 ([{book.get_author()}]) : ') or book.get_author()
            publisher = input(f'>> 출판사 ([{book.get_publisher()}]) : ') or book.get_publisher()
            price_in = input(f'>> 가격 ([{book.get_price()}]) : ')
            stock_in = input(f'>> 재고 ([{book.get_stock()}]) : ')
            price = int(price_in) if price_in.isdigit() else book.get_price()
            stock = int(stock_in) if stock_in.isdigit() else book.get_stock()
            if self.bsv.update_stock(book_no, Book(book_no, title, author, publisher, price, stock)):
                print('도서 정보를 수정했습니다.')
            else:
                print('수정에 실패했습니다.')

        def menu_remove_book(self):
            print('>>>>>>> 도서 판매 중단 및 삭제 <<<<<<<<')
            self.menu_list_books()
            book_no = self.input(int('>> 삭제할 도서번호 : '))
            if book_no is None:
                return
            if self.bsv.remove_book(book_no):
                print('도서를 삭제했습니다.')
            else:
                print('없는 도서번호입니다.')

        # 회원 관리 메뉴
        def run_admin_member_menu(self):
            print('>>>>>>> 회원 관리 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.admin_member_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_add_member_by_admin()
                elif menu == 2:
                    self.menu_list_members()
                elif menu == 3:
                    self.menu_modify_member()
                elif menu == 4:
                    self.menu_block_member()
                else:
                    print('없는 메뉴입니다.')

        def menu_add_member_by_admin(self):
            print('>>>>>>> 회원 수동 추가 <<<<<<<<')
            id = input('> 아이디 입력 : ')
            password = input('> 비밀번호 입력 : ')
            name = input('> 회원명 입력 : ')
            email = input('> 이메일 입력 : ')
            address = input('> 주소 입력 : ')
            if self.msv.register_member_by_admin(Member(id, password, name, email, address)):
                print('회원을 추가했습니다.')
            else:
                print('회원 추가에 실패했습니다.')

        def menu_list_members(self):
            print('>>>>>>> 회원 목록 및 상세 조회 <<<<<<<<')
            members = self.msv.view_all_members()
            if not members:
                print('가입한 회원이 없습니다. ')
                return
            for member in members:
                print(member)
            id = input('>> 상세 조회할 아이디 : ')
            if id:
                member = self.msv.get_member_info(id.lower())
                if member:
                    print('[상세]', member)
                else:
                    print('회원이 아닙니다.')

        def menu_modify_member(self):
            print('>>>>>>> 회원 정보 수정 <<<<<<<<')
            id = input('>> 수정할 회원 아이디 : ').lower()
            member = self.msv.get_member_info(id)
            if not member:
                print('없는 회원입니다.')
                return
            name = input(f'>> 회원명 ([{member.get_name()}]) : ') or member.get_name()
            email = input(f'>> 이메일 ([{member.get_email()}]) : ') or member.get_email()
            address = input(f'>> 주소 ([{member.get_address()}]) : ') or member.get_address()
            member.set_name(name)
            member.set_email(email)
            member.set_address(address)
            if self.msv.modify_memver_profile(id, member):
                print('회원 정보를 수정했습니다.')
            else:
                print('수정에 실패했습니다. ')

        def menu_block_member(self):
            print('>>>>>>> 회원 탈퇴 처리 및 제재 <<<<<<<<')
            id = input('>> 탈퇴/제재할 회원 아이디 : ').lower()
            if self.msv.block_member(id):
                print('탈퇴 처리되었습니다.')
            else:
                print('처리에 실패했습니다.')
        
        # 주문 관리 메뉴
        def run_admin_order_menu(self):
            print('>>>>>>> 주문관리 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.admin_order_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_list_all_orders()
                elif menu == 2:
                    self.menu_view_order_detail()
                elif menu == 3:
                    self.menu_manage_order_status()
                elif menu == 4:
                    self.menu_cancel_order()
                else:
                    print('없는 메뉴 입니다.')

        def menu_list_all_orders(self):
            print('>>>>>>> 주문 목록 조회 <<<<<<<<')
            orders = self.osv.get_order_info()
            if not orders:
                print('주문 내역이 없습니다.')
                return
            for order in orders:
                print(order)

        def menu_view_order_detail(self):
            print('>>>>>>> 주문 상세 조회 <<<<<<<<')
            order_no = self.input(int('>> 주문번호 : '))
            if order_no is None:
                return
            order = self.osv.get_order(order_no)
            if not order:
                print(' 없는 주문번호입니다. ')
                return
            print(order)
            for item in self.osv.get_order_item(order_no):
                book = self.bsv.get_book_info(item.get_book_no())
                title = book.get_title() if book else '(삭제된 도서)'
                print(f'  - {title}\t{item}')

        def menu_manage_order_status(self):
            print('>>>>>>> 주문 상태 관리(배송) <<<<<<<<')
            order_no = self.input(int('>> 주문 번호 : '))
            if order_no is None:
                return
            delivery = self.dsv.view_delivery_status_by_order(order_no)
            if not delivery:
                print('해당 주문의 배송 정보가 없습니다.')
                return
            print(f'현재 상태 : {delivery.get_delivery_status()}')
            status_list = [Delivery.READY, Delivery.SHIPPING, Delivery.DONE]
            for i, s in enumerate(status_list, 1):
                print(f'{i}. {s}')
            sel = self.input(int('>> 변경할 상태 : '))
            if sel is None or sel < 1 or sel > len(status_list):
                print('잘못된 선택입니다.')
                return
            if self.dsv.update_delivery_status(delivery.get_delivery_no(), status_list[sel - 1]):
                print('배송 상태를 변경했습니다. ')
        
        def menu_cancel_order(self):
            print('>>>>>>> 주문 취소 및 환불 <<<<<<<<')
            order_no = self.input(int('>> 취소할 주문 번호 : '))
            if order_no is None:
                return
            order = self.osv.get_order(order_no)
            if not order:
                return
             #재고 복구
            for item in self.osv.get_order_item(order_no):
                self.bsv.restore_stock(item.get_book_no(), item.get_count())
            # 배송 취소 + 주문 취소
            self.dsv.cancel_delivery_by_order(order_no)
            if self.osv.cancel_order(order_no):
                print(f'주문번호 {order_no}를 취소(환불)했습니다.')
            else:
                print('주문 취소에 실패했습니다.')

        # 배송 관리 메뉴
        def run_admin_delivery_menu(self):
            print('>>>>>>> 배송 관리 <<<<<<<<')
            while True:
                menu = self.select_menu(OnlineBookStore.admin_delivery_menu)
                if menu == 0:
                    break
                elif menu == 1:
                    self.menu_list_all_deliveries()
                elif menu == 2:
                    self.menu_view_member_deliveries()
                elif menu == 3:
                    self.menu_change_delivery_status()
                elif menu == 4:
                    self.menu_return_deliverty()
                else:
                    print('없는 메뉴입니다.')
                    
        def menu_list_all_deliveries(self):
            print('>>>>>>> 배송 목록 조회 <<<<<<<<')
            deliveries = self.dsv.view_all_deliveries()
            if not deliveries:
                print('배송 정보가 없습니다.')
                return
            for delivery in deliveries:
                print(delivery)
        
        def menu_view_member_deliveries(self):
            print('>>>>>>> 회원별 배송 상세 조회 <<<<<<<<')
            id = input(' >> 회원 아이디 :').lower()
            orders = self.osv.get_order_info(id)
            if not orders:
                print('해당 회원의 주문/배송 내역이 없습니다.')
                return
            for order in orders:
                delivery = self.dsv.view_delivery_status_by_order(order.get_order_no())
                if delivery:
                    print(delivery)
        
        def menu_change_delivery_status(self):
            print('>>>>>>> 배송 상태 변경 <<<<<<<<')
            delivery_no = self.input(int('>> 배송 번호 : '))
            if delivery_no is None:
                return
            status_list = [Delivery.READY, Delivery.SHIPPING, Delivery.DONE]
            for i, s in enumerate(status_list, 1):
                print(f'{i}. {s}')
            sel = self.input_int('>> 변경할 상태 : ')
            if sel is None or sel < 1 or sel > len(status_list):
                print('잘못된 선택입니다.')
                return
            if self.dsv.update_delivery_status(delivery_no, status_list[sel - 1]):
                    print('배송 상태를 변경했습니다.')
            else:
                    print('없는 배송번호입니다.')

        def menu_return_delivery(self):
            print('>>>>>>> 배송 취소 및 반품 회수 등록 <<<<<<<<')
            delivery_no = self.input(int(' >> 배송번호 : '))
            if delivery_no is None:
                return
            print('1. 배송취소 2. 반품 회수 등록')
            sel = self.input(int('>> 선택 : '))
            if sel == 1:
                status = Delivery.CANCELED
            elif sel == 2:
                status = Delivery.RETURNED
            else:
                print('없는 메뉴입니다.')
                return
            if self.dsv.update_delivery_status(delivery_no, status):
                print(f'배송 상태를 [{status}](으)로 변경했습니다.')
            else:
                print('없는 배송번호 입니다.')
            

if __name__ == '__main__':
    app = OnlineBookStore()
    app.main()
            


            

                



