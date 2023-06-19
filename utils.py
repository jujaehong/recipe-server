from passlib.hash import pbkdf2_sha256
from config import Config

# 1. 원문 비밀번호를, 단방향으로 암호화 하는 함수.
def hash_password(original_password) : 
    password = pbkdf2_sha256.hash(original_password + Config.SALT) # 암호의 패턴화를 방지하기 위해서 아무문자도 같이 붙여서 한꺼번에 암호화 한다.
    return password 

# 2. 유저가 입력한 비번이, 맞는지 체크하는 함수
def check_password(original_password, hash_password):
    check =  pbkdf2_sha256.verify(original_password + Config.SALT ,hash_password) # 오리지널 비밀번호 + 패턴방지문자  , 암호화된 비밀번호
    return check