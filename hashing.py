from passlib.context import CryptContext
                        
pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

class hash():
    def hash_pass(password:str):
        hashed_pass= pwd_context.hash(password)
        return hashed_pass
    
    def verify(plain_pass, hash_pass):
        return pwd_context.verify(plain_pass, hash_pass)