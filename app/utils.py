from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def getHash(str):
    return pwd_context.hash(str)

def verify(attempted_password, hashed_password):
    return pwd_context.verify(attempted_password, hashed_password)