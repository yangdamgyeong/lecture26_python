from Account.account import Account
from Account.account_dao import AccountDAO

class AccountService:
    account_no_seq = 111111

    def __init__(self, account_dao):
        self.__dao = account_dao

    def create_account(self, account):
        #계좌번호를 생성하여 반영
        account.set_account_no(str(AccountService.account_no_seq))
        AccountService.account_no_seq += 1
        return self.__dao.insert_account(account)

    def get_all_accounts(self):
        return self.__dao.select_all_accounts()

    def get_members_accounts(self, id):
        return self.__dao.select_accounts_by_member_id(id)

    def deposit(self, account_no, amount):
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            new_balance = account.get_balance() + amount
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        return False
    
    def withdraw(self, id, account_no, amount, password):
        # 마이너스 지원 안함
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            if account.get_owner() != id and account.get_password() != password:
                raise KeyError
            new_balance = account.get_balance() - amount
            if new_balance < 0:
                raise ValueError
            account.set_balance(new_balance)
            return self.__dao.update_account(account_no, account)
        return False

    def delete_account(self, id, account_no, password):
        account = self.__dao.select_account_by_account_no(account_no)
        if not account:
            return False
        if account.get_owner() != id or account.get_password() != password:
            raise KeyError
        return self.__dao.delete_account(account_no)
 
    def get_account_balance(self, account_no):
        account = self.__dao.select_account_by_account_no(account_no)
        if account:
            return account.get_balance()
        return -1

if __name__ == '__main__':
    aservice = AccountService(AccountDAO())
    aservice.create_account(Account(0, 'yangdam', 100000, '1234'))
    aservice.create_account(Account(0, 'yangdam', 200000, '1234'))
    aservice.create_account(Account(0, 'damgyeong', 300000, '1234'))
    for account in aservice.get_all_accounts():
        print(account)
    for account in aservice.get_members_accounts('yangdam'):
        print(account)

    aservice.deposit('111113', 100000)
    print()
    for account in aservice.get_members_accounts('damgyeong'):
        print(account)
    print()
    if aservice.deposit('111114', 100000):
        for account in aservice.get_all_accounts():
            print(account)
    else:
        print('없는 계좌입니다.')
    try:
        aservice.withdraw('yangdam', '111112', 100000, '1234')
    except Exception as e:
        print(type(e))
    else:
        for account in aservice.get_all_accounts():
            print(account)

    try:
        aservice.delete_account('yangdam', '111112', '1111')
    except Exception as e:
        print(type(e))
    else:
        for account in aservice.get_all_accounts():
            print(account)