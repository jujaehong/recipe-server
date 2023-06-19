from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from mysql_connection import get_connection

from email_validator import validate_email, EmailNotValidError

class UserRegisterResource(Resource):
    
    def post(self) :

        # {
        #     "username" : "홍길동", 
        #     "email" : "abc@naver.com",
        #     "password" : "1234"
        # }
        
        # 1. 클라이언트가 보낸 데이터를 받아준다.

        data = request.get_json()  # 클라이언트가 보내는 내용 (username, email, password )

        # 2. 이메일 주소형식이 올바른지 확인한다.
        try :
            validate_email( data['email'] ) 
        except EmailNotValidError as e :
            return {'result' : 'fale', 'error' : str(e)}, 400 # 400은 http 상태코드

        # 3. 비밀번호 길이가 유효한지 체크한다.
        #    만약, 비번이 4자리 이상, 12자리 이하라고 한다면,

        if len(data['password']) < 4 or len(data['password']) > 12 :
            return {'result' : 'fale', 'error' : '비번 길이 에러'}, 400

        return
    