from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
import datetime


# 로그아웃
## 로그아웃된 토큰을 저장할 set을 만든다.
jwt_blocklist = set()

class UserLogoutResource(Resource):
    @jwt_required() # header에 토큰 붙여주는 거
    def delete(self) : 
        jti = get_jwt()['jti']
        print(jti)
        jwt_blocklist.add(jti)
         # 헤더에서 블락리스트를 가져와서 jwt_blocklist에 넣어
        return {'result':'success'}
    
    # headers에 value에 Bearer+한칸띄우고+토큰이름 입력해서 jwt 전달 
    

class UserRegisterResource(Resource):
    # 플라스크의 리소스를 상속받아서 http 메소드들을 사용하겠다. 
    # 클래스는 변수와 함수의 묶음!
    def post(self): 
        # 이게 아래의 data임.
        # {
        #     "username": "홍길동",
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }
        # 1. 클라이언트가 보낸 데이터를 받아준다. 
        # body 부분의 json
        data = request.get_json() #함수 동작은 매뉴얼에 들어있다. 
        # 인간의 요청은 대체로 두루뭉술함 컴퓨터 입장에서 절차와 방법을 만들어주세요.
        # 2. 이메일 주소 형식이 올바른지 확인한다. 이메일 체크하는 라이브러리가 엄청 많다. 찾아서 쓰면 됨 email-validator
        try : 
            validate_email( data['email'] )
        except EmailNotValidError as e :
            print(e) # 디버깅할 때 필요하니까 넣어두세요
            return {'result':'fail', 'error':str(e)}, 400 # 400:bad request
        
        # 3. 비밀번호 길이가 유효한지 체크한다. 
        # 만약 비번이 4자리 이상, 12자리 이하라고 한다면, 
        if len( data['password'] ) < 4 or len( data['password'] ) > 12 : # 비정상이면 체크하고 리턴하고 끝내는 것이 맞음 그래서 비정상 체크 
            return {'result':'fail', 'error':'비번 길이 에러'}, 400
            # 클라이언트 개발자도 데이터 제대로 들어가는지 체크한다. 데이터무결성과 보안이 중요하니까. 해킹 요청 시도 : d-dos 공격 서버에 요청이 많아서 다운시킴. 

        # 4. 비밀번호를 암호화한다. 보안 때문에 중요하다. 
        hashed_password = hash_password( data['password'] )
        print(hashed_password)

        # 5. DB에 이미 있는지 확인한다. 
        try : 
            connection = get_connection()
            query = '''select * from user
                    where email = %s;'''
            record = ( data['email'], )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            print(result_list)

            if len( result_list )== 1 :
                return {'result':'fail', 'error':'이미 회원가입 한 사람'}, 400 
            
            # 기존 회원이 아니므로 회원가입시킴 
            # DB에 저장한다. 
            query ='''insert into user
                    (username, email, password)
                    values
                    (%s, %s, %s);'''
            record = ( data['username'], data['email'], hashed_password)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit() 

            ### DB에 데이터를 insert 한 후에, 
            ### 그 인서트 된 행의 아이디를 가져오는 코드 !! 
            #### 반드시 커밋 후 실행해야 함 ^^
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}, 500 # 500:서버 쪽 문제
        
        #create_access_token(user_id, expires= datetime.timedelta(days=))
        access_token = create_access_token(user_id)
        return {'result':'success', 'access token': access_token}, 200 # 문제 없음. 생략 가능. 



#### 로그인 관련 개발 

class UserLoginResource(Resource):
    def post(self): 
        # 1. 클라이언트로부터 데이터 받아옴
        data = request.get_json() # body에 있는 제이슨 받아와요
        try :
            # 2. 이메일 주소로, DB에 select 한다.
            connection = get_connection()
            query = '''select * from user
                    where email = %s;'''
            record = ( data['email'], )
            cursor = connection.cursor( dictionary=True )
            cursor.execute( query, record )
            result_list = cursor.fetchall()

        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}, 500 # 500:서버 쪽 문제

        # 데이터가 없을 때가 이상하다. 
        if len( result_list ) == 0 : 
            return {'result':'fail', 'error':'회원가입한 사람이 아닙니다'}, 400
            

        # 3. 비밀번호가 일치하는 지 확인한다. 암호화된 비밀번호가 일치하는지 확인해야 함. 
        # print(result_list)
        check = check_password( data['password'], result_list[0]['password'])
        if check == False : 
            return {'result':'fail', 'error':'비번 틀림'}, 400

        # 4. 클라이언트에게 데이터를 보내준다. 
        access_token = create_access_token(result_list[0]['id'])
        return {'result':'success', 'access token': access_token }

