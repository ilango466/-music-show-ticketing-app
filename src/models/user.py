from src.db.connection_pool import get_connection
from src.db.database import Database

class User:
    def __init__(self, name, email, password='***', user_id=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        with get_connection() as connection:
            user_id = Database().add_new_user(connection, (self.name, self.email, self.password))
            if user_id is not None:
                self.user_id = user_id
                print(f"User '{self.name}' saved with ID: {self.user_id}")

    @classmethod
    def all(cls):
        with get_connection() as connection:
            users = Database().get_all_users(connection)
            return [cls(user[1], user[2], user[3], user[0]) for user in users]
    
    @classmethod
    def get_user_by_mail(cls,user_email):   
        with get_connection() as connection:
            user = Database().get_one_user_by_mail(connection,user_email)
            print( user, user is None)
            if  user is None:
                return user
            user_obj =  cls(user[1], user[2], user_id = user[0])
            return user_obj
    
    @staticmethod
    def is_exists(email, passsword):   
        with get_connection() as connection:
            user = Database().check_user(connection,email,passsword)
            return user is not None

    def __repr__(self) -> str:
        return f"User({self.user_id}, '{self.name}')"