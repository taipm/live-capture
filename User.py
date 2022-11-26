import re
from MongoDb import ObjectDb

EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(input:str):
    return re.match(EMAIL_FORMAT,input) is not None

class User(ObjectDb):
    def __init__(self, user_name) -> None:
        super().__init__()
        self.userName = user_name
        self._email = None

    @property
    def email(self):
        return self._email
        
    @email.setter
    def email(self, new_email):
        if not is_valid_email(new_email):
            raise ValueError(f"Can't set {new_email} as it's not a valid email")
        self._email = new_email

# u = User(user_name='taipm')
# u.email = 'taipm@bidv.com.vn'
# print(u.email)

# u.email = 'taipm-bidv.com.vn'
# print(u.email)