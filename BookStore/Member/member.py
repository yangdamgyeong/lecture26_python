class Member:
    def __init__(self, id, password, name, email, address):
        self.__member_no = 0
        self.__id = id
        self.__password = password
        self.__name = name
        self.__email = email
        self.__address = address

    def get_member_no(self):
        return self.__member_no    
    def get_id(self):
        return self.__id
    def get_password(self):
        return self.__password
    def get_name(self):
        return self.__name
    def get_email(self):
        return self.__email
    def get_address(self):
        return self.__address
    
    def set_email(self):
        self.__email
    def set_address(self):
        self.__address
    
    def __str__(self):
        return f'{self.__member_no}\t{self.__id}\t{self.__name}\t{self.__email}\t{self.__address}'