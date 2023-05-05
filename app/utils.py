from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_pass,harsh_pass):#fun gives the value of true or false
    return pwd_context.verify(plain_pass, harsh_pass)# verifies by converting the raw pass into hash and compare it woyh the one alr present in database
