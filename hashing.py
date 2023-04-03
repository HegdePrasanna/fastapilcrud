from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash():
    def hashing_pd(password: str):
        return pwd_context.hash(password)
